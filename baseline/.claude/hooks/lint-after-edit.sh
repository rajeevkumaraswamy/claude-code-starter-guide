#!/usr/bin/env bash
# PostToolUse hook (matcher "Edit|Write"): lint-fix and format the Python file
# Claude just edited or wrote.
#   exit 0 = clean, or not a .py file
#   exit 2 = problems ruff could not fix; stderr is shown to Claude so it fixes them
#   exit 1 = hook could not run (e.g. uv missing); you see a warning, Claude carries on
set -u

file=$(python3 -c '
import json, sys
try:
    data = json.load(sys.stdin)
except ValueError:
    sys.exit(0)
print((data.get("tool_input") or {}).get("file_path") or "")
')

case "$file" in
  *.py) ;;
  *) exit 0 ;;
esac
[ -f "$file" ] || exit 0

if ! command -v uv >/dev/null 2>&1; then
  echo "lint-after-edit: uv not found on PATH; skipped ruff on $file" >&2
  exit 1
fi

cd "${CLAUDE_PROJECT_DIR:-.}" || exit 1

# Fix first, then format: fixes such as import sorting and removing unused
# imports can leave blank lines that only the formatter cleans up. The last
# check reports what is left, with line numbers matching the final file.
# (A syntax error makes the first two fail quietly; the last check reports it.)
uv run --quiet ruff check --fix --quiet "$file" >/dev/null 2>&1
uv run --quiet ruff format --quiet "$file" >/dev/null 2>&1

if ! out=$(uv run --quiet ruff check --quiet "$file" 2>&1); then
  {
    echo "ruff found problems in $file that it could not fix automatically. Fix them:"
    printf '%s\n' "$out"
  } >&2
  exit 2
fi
exit 0
