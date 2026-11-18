"""Tests for tools/check_guide.py. Run: uv run --with pytest pytest tools/tests/test_check_guide.py"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import check_guide

LEDGER = r"""# Ledger

| id | feature | exact syntax | doc URL | verified | notes |
| :- | :- | :- | :- | :- | :- |
| `/init` | Generate | `/init` | u | d | n |
| `claude doctor` | Diag | `claude doctor` | u | d | n |
| `claude -p` | Print | `claude -p "q"` | u | d | n |
| `curl -fsSL https://claude.ai/install.sh \| bash` | Install | x | u | d | n |
| `/old` | Gone | REMOVED | u | d | REMOVED: do not teach |
| `/a` / `/b` | Aliased | x | u | d | n |

## Schema details

| other | table |
| :- | :- |
| `/notanid` | x |
"""


def make_repo(tmp_path, guide_text=None, ledger=LEDGER):
    (tmp_path / "tools").mkdir()
    (tmp_path / "tools" / "feature-ledger.md").write_text(ledger)
    if guide_text is not None:
        (tmp_path / "guide").mkdir()
        (tmp_path / "guide" / "01.md").write_text(guide_text)
    return tmp_path


def run(tmp_path, capsys):
    code = check_guide.main(tmp_path)
    return code, capsys.readouterr().out


def test_unknown_slash_command_fails(tmp_path, capsys):
    code, out = run(make_repo(tmp_path, "Run `/foo` now.\n"), capsys)
    assert code == 1
    assert "/foo" in out
    assert "guide/01.md:1:" in out


def test_known_slash_command_passes(tmp_path, capsys):
    code, out = run(make_repo(tmp_path, "Run `/init` now, or `/init extra`.\n"), capsys)
    assert (code, out) == (0, "")


def test_removed_command_fails(tmp_path, capsys):
    code, out = run(make_repo(tmp_path, "Use `/old`.\n"), capsys)
    assert code == 1
    assert "REMOVED" in out


def test_broken_link_fails(tmp_path, capsys):
    code, out = run(make_repo(tmp_path, "See [x](nope.md#top).\n"), capsys)
    assert code == 1
    assert "nope.md" in out


def test_good_link_and_external_and_anchor_pass(tmp_path, capsys):
    repo = make_repo(
        tmp_path, "[a](02.md#s) [b](https://x.io) [c](#here) [d](mailto:a@b.c)\n"
    )
    (repo / "guide" / "02.md").write_text("hi\n")
    assert run(repo, capsys)[0] == 0


def test_missing_practice_path_fails(tmp_path, capsys):
    code, out = run(make_repo(tmp_path, "Open `practice/x.py`.\n"), capsys)
    assert code == 1
    assert "practice/x.py" in out


def test_existing_path_with_line_and_test_suffix_passes(tmp_path, capsys):
    repo = make_repo(tmp_path, "`practice/x.py:12` and `practice/x.py::test_a`\n")
    (repo / "practice").mkdir()
    (repo / "practice" / "x.py").write_text("")
    assert run(repo, capsys)[0] == 0


def test_missing_checkpoint_fails(tmp_path, capsys):
    code, out = run(
        make_repo(tmp_path, "Run `checkpoints/test_session_9.py`.\n"), capsys
    )
    assert code == 1
    assert "test_session_9.py" in out


def test_escaped_pipe_ledger_id_parsed(tmp_path, capsys):
    ledger = check_guide.load_ledger(make_repo(tmp_path))
    assert "curl -fsSL https://claude.ai/install.sh | bash" in ledger
    assert "/b" in ledger and "/a" in ledger
    assert "/notanid" not in ledger
    assert ledger["/old"] is True and ledger["/init"] is False


def test_claude_subcommands(tmp_path, capsys):
    text = '`claude doctor` `claude -p "hi"` `claude` `claude --bogus`\n'
    code, out = run(make_repo(tmp_path, text), capsys)
    assert code == 1
    assert "claude --bogus" in out
    assert out.count("\n") == 1


def test_fenced_block_commands(tmp_path, capsys):
    text = "```bash\nclaude doctor\nclaude --nope\n```\n```text\n/init\n/bad\n```\n"
    code, out = run(make_repo(tmp_path, text), capsys)
    assert code == 1
    assert "claude --nope" in out and "/bad" in out
    assert "01.md:3:" in out and "01.md:7:" in out
    assert out.count("\n") == 2


def test_paths_not_slash_commands(tmp_path, capsys):
    assert (
        run(
            make_repo(tmp_path, "`/usr/bin` `/etc/x`\n```\n/usr/bin/env\n```\n"), capsys
        )[0]
        == 0
    )


def test_no_guide_dir_ok(tmp_path, capsys):
    assert run(make_repo(tmp_path), capsys) == (0, "")
