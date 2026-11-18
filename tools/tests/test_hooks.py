"""Tests for the hook scripts and settings shipped in baseline/.claude/.

Run from the repo root:  uv run --with pytest pytest tools/tests/test_hooks.py

Each hook test builds a tiny uv project in tmp_path (pyproject with pytest and ruff
as dev dependencies, one module, one test), copies baseline/.claude into it, and
pipes hook JSON into the script exactly as Claude Code does. Needs bash, python3, uv.
"""

import json
import os
import re
import shutil
import subprocess
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[2]
BASELINE = REPO / "baseline"
HOOKS = BASELINE / ".claude" / "hooks"
SETTINGS = BASELINE / ".claude" / "settings.json"

PYPROJECT = """\
[project]
name = "hookdemo"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = []

[dependency-groups]
dev = ["pytest", "ruff"]

[tool.ruff.lint]
select = ["E", "F", "I"]
"""

MODULE = """\
def add(a, b):
    return a + b
"""

PASSING_TEST = """\
from calc import add


def test_add():
    assert add(2, 2) == 4
"""

FAILING_TEST = """\
from calc import add


def test_add():
    assert add(2, 2) == 5
"""


def _clean_env(project: Path) -> dict[str, str]:
    """Environment for a hook run: no leakage from the outer uv/pytest process."""
    env = {
        k: v
        for k, v in os.environ.items()
        if not k.startswith(("UV_", "VIRTUAL_ENV", "PYTEST_", "PYTHON"))
    }
    env["CLAUDE_PROJECT_DIR"] = str(project)
    return env


@pytest.fixture
def project(tmp_path: Path) -> Path:
    proj = tmp_path / "proj"
    proj.mkdir()
    (proj / "pyproject.toml").write_text(PYPROJECT)
    (proj / "calc.py").write_text(MODULE)
    (proj / "test_calc.py").write_text(PASSING_TEST)
    shutil.copytree(BASELINE / ".claude", proj / ".claude")
    return proj


def run_hook(project: Path, script: str, payload: dict | str):
    stdin = payload if isinstance(payload, str) else json.dumps(payload)
    return subprocess.run(
        [str(project / ".claude" / "hooks" / script)],
        input=stdin,
        capture_output=True,
        text=True,
        cwd=project,
        env=_clean_env(project),
        timeout=300,
    )


def edit_payload(path: Path, tool: str = "Edit") -> dict:
    return {
        "session_id": "test",
        "cwd": str(path.parent),
        "hook_event_name": "PostToolUse",
        "tool_name": tool,
        "tool_input": {"file_path": str(path)},
        "tool_response": {"filePath": str(path)},
    }


def stop_payload(active: bool = False) -> dict:
    return {
        "session_id": "test",
        "hook_event_name": "Stop",
        "stop_hook_active": active,
        "last_assistant_message": "Done.",
    }


# --- lint-after-edit.sh (PostToolUse, matcher Edit|Write) -------------------------


def test_lint_formats_py_file(project: Path):
    target = project / "messy.py"
    target.write_text("def f( x ):\n    return x+1\n")
    result = run_hook(project, "lint-after-edit.sh", edit_payload(target, "Write"))
    assert result.returncode == 0, result.stderr
    assert target.read_text() == "def f(x):\n    return x + 1\n"


def test_lint_result_is_formatted_after_fixes(project: Path):
    # Found in the live smoke test: an unused stdlib import added below a
    # third-party one is moved by isort (I001) and then removed (F401). If
    # formatting ran before the fixes, a stray blank line was left behind.
    target = project / "mod.py"
    target.write_text('"""Doc."""\n\nimport json\nimport os\n\nprint(json)\n')
    (project / "pyproject.toml").write_text(
        PYPROJECT + '\n[tool.ruff.lint.isort]\nknown-third-party = ["json"]\n'
    )
    result = run_hook(project, "lint-after-edit.sh", edit_payload(target))
    assert result.returncode == 0, result.stderr
    assert target.read_text() == '"""Doc."""\n\nimport json\n\nprint(json)\n'


def test_lint_unfixable_exit2(project: Path):
    target = project / "broken.py"
    target.write_text("def g():\n    return undefined_name + 1\n")
    result = run_hook(project, "lint-after-edit.sh", edit_payload(target))
    assert result.returncode == 2
    assert "F821" in result.stderr


def test_lint_ignores_non_py(project: Path):
    target = project / "notes.md"
    original = "```python\nimport os\ndef f( x ):\n    return undefined\n```\n"
    target.write_text(original)
    result = run_hook(project, "lint-after-edit.sh", edit_payload(target))
    assert result.returncode == 0
    assert result.stderr == ""
    assert target.read_text() == original
    # `uv run` creates .venv on first use, so no .venv means ruff never ran.
    assert not (project / ".venv").exists()


def test_lint_ignores_malformed_input(project: Path):
    result = run_hook(project, "lint-after-edit.sh", "not json")
    assert result.returncode == 0


# --- tests-before-stop.sh (Stop) ---------------------------------------------------


def test_stop_passes_when_green(project: Path):
    result = run_hook(project, "tests-before-stop.sh", stop_payload())
    assert result.returncode == 0, result.stdout + result.stderr


def test_stop_blocks_when_red(project: Path):
    (project / "test_calc.py").write_text(FAILING_TEST)
    result = run_hook(project, "tests-before-stop.sh", stop_payload())
    assert result.returncode == 2
    assert "failed" in result.stderr
    # Two header lines plus the last 30 lines of pytest output.
    assert len(result.stderr.strip().splitlines()) <= 32


def test_stop_prints_stdout_when_blocking(project: Path):
    # Claude Code treats a Stop hook that exits 2 with EMPTY stdout and
    # "No such file or directory" on stderr as non-blocking. Pytest output can
    # contain that phrase, so the script must always say something on stdout.
    (project / "test_calc.py").write_text(
        "def test_missing_file():\n    open('does-not-exist.txt')\n"
    )
    result = run_hook(project, "tests-before-stop.sh", stop_payload())
    assert result.returncode == 2
    assert "No such file or directory" in result.stderr
    assert result.stdout.strip() != ""
    assert not result.stdout.lstrip().startswith("{")  # plain text, not JSON


def test_stop_no_loop(project: Path):
    (project / "test_calc.py").write_text(FAILING_TEST)
    result = run_hook(project, "tests-before-stop.sh", stop_payload(active=True))
    assert result.returncode == 0
    assert not (project / ".venv").exists()  # pytest was not even run


# --- settings.json -----------------------------------------------------------------


def test_settings_json_valid():
    settings = json.loads(SETTINGS.read_text())
    allow = settings["permissions"]["allow"]
    deny = settings["permissions"]["deny"]
    hooks = settings["hooks"]
    assert allow and deny and hooks

    for rule in [
        "Bash(uv run pytest *)",
        "Bash(uv run ruff *)",
        "Bash(git status *)",
        "Bash(git diff *)",
        "Bash(git log *)",
        "Bash(gh pr view *)",
        "Bash(gh pr diff *)",
    ]:
        assert rule in allow
    assert not any(":*" in rule for rule in allow), "use ' *', not legacy ':*'"
    assert any(r.startswith("Read(") and ".env" in r for r in deny)
    assert any(r.startswith("Read(") and "secrets/**" in r for r in deny)

    assert set(hooks) == {"PostToolUse", "Stop"}
    assert [g["matcher"] for g in hooks["PostToolUse"]] == ["Edit|Write"]

    commands = [
        h["command"] for groups in hooks.values() for g in groups for h in g["hooks"]
    ]
    assert len(commands) == 2
    for command in commands:
        assert "CLAUDE_PROJECT_DIR" in command
        match = re.search(r"/\.claude/hooks/([\w.-]+)", command)
        assert match, command
        script = HOOKS / match.group(1)
        assert script.is_file(), script
        assert os.access(script, os.X_OK), f"{script} is not executable"


# --- destructive git deny rules -------------------------------------------------------
#
# Matching follows https://code.claude.com/docs/en/permissions#wildcard-patterns and
# #compound-commands: a Bash rule matches the whole command text; `*` matches any text
# including spaces; everything else is literal; a trailing ` *` that is the rule's only
# wildcard also matches the bare command; deny rules apply when ANY subcommand of a
# compound command (split on && || ; | |& & newline) matches, and match past a leading
# VAR=value assignment. The helper only handles simple commands without quoting.

DESTRUCTIVE_GIT_DENY = [
    "Bash(git checkout -- *)",
    "Bash(git checkout * -- *)",
    "Bash(git checkout . *)",
    "Bash(git restore *)",
    "Bash(git reset --hard *)",
    "Bash(git clean *)",
]


def _bash_pattern(rule: str) -> str | None:
    m = re.fullmatch(r"Bash\((.*)\)", rule)
    return m.group(1) if m else None


def _rule_matches(pattern: str, command: str) -> bool:
    regex = ".*".join(re.escape(part) for part in pattern.split("*"))
    if re.fullmatch(regex, command):
        return True
    if pattern.endswith(" *") and pattern.count("*") == 1:
        return command == pattern[:-2]
    return False


def _subcommands(command: str) -> list[str]:
    parts = re.split(r"\|&|&&|\|\||;|\||&|\n", command)
    out = []
    for part in parts:
        part = part.strip()
        part = re.sub(r"^(?:[A-Za-z_][A-Za-z0-9_]*=\S*\s+)+", "", part)
        if part:
            out.append(part)
    return out


def _denied(command: str, deny: list[str]) -> bool:
    patterns = [p for p in map(_bash_pattern, deny) if p is not None]
    return any(_rule_matches(p, sub) for sub in _subcommands(command) for p in patterns)


@pytest.mark.parametrize(
    ("pattern", "command", "expected"),
    [  # rows from the docs' wildcard table, to check the helper itself
        ("npm run build", "npm run build", True),
        ("npm run build", "npm run build --watch", False),
        ("npm run *", "npm run", True),
        ("npm run *", "npm install", False),
        ("git log * main", "git log --oneline main", True),
        ("git log * main", "git log main", False),
        ("ls *", "ls", True),
        ("ls *", "lsof", False),
        ("ls*", "lsof", True),
        ("* --help *", "npm --help x", True),
        ("* --help *", "npm --help", False),
    ],
)
def test_matcher_reproduces_docs_table(pattern, command, expected):
    assert _rule_matches(pattern, command) is expected


def _settings_permissions() -> tuple[list[str], list[str]]:
    perms = json.loads(SETTINGS.read_text())["permissions"]
    return perms["allow"], perms["deny"]


def test_deny_lists_destructive_git_rules():
    allow, deny = _settings_permissions()
    for rule in DESTRUCTIVE_GIT_DENY:
        assert rule in deny
    # An allow rule can't carve out of a deny rule, so a broader allow is a mistake.
    for a in map(_bash_pattern, allow):
        a_prefix = a.split("*")[0]
        for d in map(_bash_pattern, DESTRUCTIVE_GIT_DENY):
            assert not d.startswith(a_prefix), f"allow {a!r} overlaps deny {d!r}"
            assert not _rule_matches(a, d.replace("*", "x")), (a, d)


def test_allow_keeps_read_only_git():
    allow, _ = _settings_permissions()
    for rule in ["Bash(git status *)", "Bash(git diff *)", "Bash(git log *)"]:
        assert rule in allow


@pytest.mark.parametrize(
    "command",
    [
        "git checkout -- src/sensorlog/clean.py",
        "git checkout --",
        "git checkout HEAD -- src/sensorlog/clean.py",
        "git checkout .",
        "git restore src/sensorlog/clean.py",
        "git restore .",
        "git restore --staged tests/test_clean.py",  # harmless, blocked by choice
        "git reset --hard",
        "git reset --hard HEAD~1",
        "git clean -fd",
        "git clean",
        "cd practice && git reset --hard",
        "git status; git clean -f",
        "GIT_PAGER=cat git checkout -- x.py",
    ],
)
def test_destructive_git_is_denied(command):
    _, deny = _settings_permissions()
    assert _denied(command, deny)


@pytest.mark.parametrize(
    "command",
    [
        "git checkout -b feature/outliers",
        "git checkout main",
        "git switch main",
        "git switch -c feature/outliers",
        "git status",
        "git diff tests/",
        "git log --oneline -5",
        "git add tests/test_clean.py",
        "git commit -m 'feat: flag outliers'",
        "git reset HEAD tests/test_clean.py",
        "git reset --soft HEAD~1",
        "uv run pytest -q",
    ],
)
def test_everyday_git_is_not_denied(command):
    _, deny = _settings_permissions()
    assert not _denied(command, deny)
