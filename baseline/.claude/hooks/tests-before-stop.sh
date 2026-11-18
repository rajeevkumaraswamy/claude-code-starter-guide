#!/usr/bin/env bash
# Stop hook: run the test suite when Claude tries to finish its turn.
#   exit 0 = tests pass (or none collected yet): Claude may stop
#   exit 2 = tests fail: Claude keeps working; stderr (last 30 lines) is the reason
# If Claude is already continuing because of this hook (stop_hook_active is true)
# we exit 0 straight away, so it can never loop.
set -u

active=$(python3 -c '
import json, sys
try:
    data = json.load(sys.stdin)
except ValueError:
    data = {}
print("true" if isinstance(data, dict) and data.get("stop_hook_active") is True else "false")
')
[ "$active" = "true" ] && exit 0

if ! command -v uv >/dev/null 2>&1; then
  echo "tests-before-stop: uv not found on PATH; tests not run" >&2
  exit 1
fi

cd "${CLAUDE_PROJECT_DIR:-.}" || exit 1

out=$(uv run --quiet pytest -q 2>&1)
status=$?

# 0 = all passed, 5 = no tests collected (nothing to enforce yet).
if [ "$status" -eq 0 ] || [ "$status" -eq 5 ]; then
  exit 0
fi

# Always print something on stdout. Claude Code treats a Stop hook that exits 2
# with empty stdout and "No such file or directory" on stderr as a non-blocking
# error, and pytest output can contain that phrase.
echo "tests-before-stop: 'uv run pytest -q' failed (exit $status); asking Claude to keep working"
{
  echo "Tests are failing. Do not stop yet: fix the cause until 'uv run pytest -q' passes, then show the output."
  echo "Do not weaken or delete a test to make it pass; if a test itself looks wrong, say why and ask. Last 30 lines:"
  printf '%s\n' "$out" | tail -n 30
} >&2
exit 2
