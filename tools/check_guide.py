"""Guide consistency checker.

Run from the repo root:  uv run --with pytest python tools/check_guide.py .

Scans guide/*.md, every .md file under baseline/, and every .claude/settings.json
under baseline/ (.sh files are not scanned), and reports, one per line as
`file:line: message`, anything that is not backed by the ledger or the repo.
Exit code is 1 if any problem was found, else 0. A missing guide/ is fine.

Ledger (tools/feature-ledger.md)
- Only the first table (header starts `| id |`) counts; later tables are ignored.
- Rows are split on `|` not preceded by a backslash; `\\|` is unescaped to `|`.
- The id cell has its backticks removed. One cell may hold several ids,
  separated by ` / ` or `, `; each becomes its own id.
- A row is REMOVED if the word REMOVED appears in its feature or notes cell.
  Using a REMOVED id is an error.

Command matching (regex based, outside and inside code)
- Inline code spans (`...`) outside fenced blocks:
  * `/word` or `/word args` -> id `/word`. A span whose first word contains a
    second `/` (e.g. `/usr/bin`) is a path, not a command.
  * `claude <x> ...` -> id `claude <x>` where x is the first token (a
    subcommand or flag, e.g. `claude doctor`, `claude -p`). Bare `claude`
    needs no entry. For flags the bare id (`--model`, `-p`) is accepted as
    well as `claude --model`. Aliases (`claude -c`) need their own id to be taught.
- Fenced ``` blocks: a line starting (after optional indent and `$ `) with
  `claude <x>` is checked like the above, and a line starting with `/word`
  (a prompt typed into Claude) is checked as a slash command. Nothing else in a
  fence is checked.

Settings files
- Each top-level key, and each event name under `hooks`, must appear as a plain
  substring somewhere in the ledger file. Misses are reported as
  `path:1: settings key 'X' not in the feature ledger`.

Paths and links
- Inline code spans starting with practice/, baseline/, guide/ or tools/ must
  exist under the repo root (first whitespace-separated token; a trailing
  `:line` or `::test` suffix is stripped; tokens with <, >, * or { are
  treated as patterns and skipped).
- A span `checkpoints/test_session_N.py` must exist at practice/checkpoints/.
- Relative Markdown links `[x](path)` (not scheme:, not #anchor) must exist
  relative to the file; any #anchor is stripped.
"""

import json
import re
import sys
from pathlib import Path

PATH_PREFIXES = ("practice/", "baseline/", "guide/", "tools/")
SPAN = re.compile(r"(?<!`)`([^`\n]+)`(?!`)")
LINK = re.compile(r"\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
SLASH = re.compile(r"^/([A-Za-z][\w:-]*)(?:\s|$)")
CLAUDE = re.compile(r"^claude\s+(-{0,2}[A-Za-z][\w-]*)")
FENCE_CLAUDE = re.compile(r"^\s*(?:\$\s+)?(claude\s+-{0,2}[A-Za-z][\w-]*)")
CHECKPOINT = re.compile(r"^checkpoints/test_session_\d+\.py$")


def split_row(line: str) -> list[str]:
    cells = re.split(r"(?<!\\)\|", line.strip())
    return [c.strip().replace("\\|", "|") for c in cells[1:-1]]


def load_ledger(root: Path) -> dict[str, bool]:
    """Return {id: is_removed} from the first table of the ledger."""
    ledger: dict[str, bool] = {}
    in_table = False
    for line in (root / "tools" / "feature-ledger.md").read_text().splitlines():
        if not line.startswith("|"):
            if in_table:
                break
            continue
        cells = split_row(line)
        if not in_table:
            in_table = bool(cells) and cells[0] == "id"
            continue
        if not cells or set(cells[0]) <= set(":- "):
            continue
        removed = "REMOVED" in cells[1] or "REMOVED" in cells[-1]
        raw = cells[0].replace("`", "")
        for part in re.split(r" / |, ", raw):
            ledger[part.strip()] = removed
    return ledger


def check_id(ledger, key, where, problems):
    bare = key.split(" ", 1)[1] if key.startswith("claude -") else None
    if bare and key not in ledger and bare in ledger:
        key = bare
    if key not in ledger:
        problems.append(f"{where}: `{key}` is not in the feature ledger")
    elif ledger[key]:
        problems.append(f"{where}: `{key}` is REMOVED in the feature ledger")


def check_file(path: Path, root: Path, ledger, problems):
    rel = path.relative_to(root)
    in_fence = False
    for n, line in enumerate(path.read_text().splitlines(), 1):
        where = f"{rel}:{n}"
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            if m := FENCE_CLAUDE.match(line):
                check_id(ledger, " ".join(m.group(1).split()), where, problems)
            elif m := SLASH.match(line.lstrip()):
                check_id(ledger, "/" + m.group(1), where, problems)
            continue
        for span in SPAN.findall(line):
            span = span.strip()
            if m := SLASH.match(span):
                check_id(ledger, "/" + m.group(1), where, problems)
            elif m := CLAUDE.match(span):
                check_id(ledger, "claude " + m.group(1), where, problems)
            check_path(span, root, where, problems)
        for target in LINK.findall(line):
            if re.match(r"^[A-Za-z][A-Za-z0-9+.-]*:", target) or target.startswith("#"):
                continue
            target = target.split("#", 1)[0]
            if target and not (path.parent / target).exists():
                problems.append(f"{where}: broken link `{target}`")


def check_settings(path: Path, root: Path, ledger_text: str, problems):
    data = json.loads(path.read_text())
    keys = list(data)
    if isinstance(data.get("hooks"), dict):
        keys += list(data["hooks"])
    for key in keys:
        if key not in ledger_text:
            rel = path.relative_to(root)
            problems.append(f"{rel}:1: settings key '{key}' not in the feature ledger")


def check_path(span: str, root: Path, where: str, problems):
    token = span.split()[0] if span.split() else ""
    if CHECKPOINT.match(token):
        token = "practice/" + token
    if not token.startswith(PATH_PREFIXES) or re.search(r"[<>*{]", token):
        return
    token = re.sub(r"::.*$|:\d+.*$", "", token)
    if not (root / token).exists():
        problems.append(f"{where}: path `{token}` does not exist")


def main(repo_root: Path) -> int:
    root = Path(repo_root).resolve()
    ledger = load_ledger(root)
    files = sorted((root / "guide").glob("*.md")) + sorted(
        (root / "baseline").rglob("*.md")
    )
    problems: list[str] = []
    for f in files:
        check_file(f, root, ledger, problems)
    ledger_text = (root / "tools" / "feature-ledger.md").read_text()
    for f in sorted((root / "baseline").rglob(".claude/settings.json")):
        check_settings(f, root, ledger_text, problems)
    for p in problems:
        print(p)
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")))
