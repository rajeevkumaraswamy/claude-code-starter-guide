# Team baseline

A starting configuration for Claude Code in a uv + pytest + ruff project. It makes
Claude check its own work from the first prompt: ruff runs after every Python edit,
and the tests run before Claude is allowed to say it is finished.

| File | What it does |
| :- | :- |
| `CLAUDE.md` | Project instructions Claude reads at the start of every session: commands, working rules, and a section for you to fill in. |
| `.claude/settings.json` | Shared permissions and hooks. Commit it so everyone gets the same setup. |
| `.claude/hooks/lint-after-edit.sh` | After Claude edits or writes a `.py` file: `uv run ruff check --fix`, then `uv run ruff format`. Anything ruff cannot fix goes back to Claude to fix. |
| `.claude/hooks/tests-before-stop.sh` | When Claude tries to finish: `uv run pytest -q`. If tests fail, Claude is told to keep working and gets the last 30 lines of output. |

## Install

Your project needs `uv`, `python3`, and pytest and ruff as dev dependencies
(`uv add --dev pytest ruff` if they are not there yet).

1. Copy both into the project root (the folder with `pyproject.toml`):

   ```bash
   cp baseline/CLAUDE.md /path/to/project/
   cp -R baseline/.claude /path/to/project/
   ```

   If the project already has a `.claude/settings.json`, merge the `permissions`
   and `hooks` blocks by hand instead of overwriting it.
2. Open `CLAUDE.md` and replace every `<PLACEHOLDER>` in "This project". Fix the
   commands at the top if your project runs them differently.
3. Commit both:

   ```bash
   git add CLAUDE.md .claude/settings.json .claude/hooks/
   git commit -m "chore: add Claude Code team baseline"
   ```

4. Start `claude` in the project root and accept the workspace trust dialog.
   Run `/hooks` to see both hooks listed.

## What the settings allow and deny

- **Allowed without asking:** `uv run pytest ...`, `uv run ruff ...`, `git status`,
  `git diff`, `git log`, `gh pr view`, `gh pr diff`. Everything else still asks.
- **Denied:** reading `.env`, `.env.*`, and anything under a `secrets/` directory.

## Things to know

- **Nothing runs until you trust the folder.** In an interactive session Claude Code
  holds back all hooks, and the `allow` rules above, until you accept the workspace
  trust dialog for the folder. Deny rules apply straight away. A headless
  `claude -p` run never shows the dialog: the hooks run there, but the `allow`
  rules are still ignored until the folder has been trusted once interactively.
- **The Stop hook pushes back once per turn.** If tests fail, Claude keeps working.
  If it tries to stop again while they still fail, the hook lets it stop, so it
  cannot loop forever. Read what Claude says about the failure.
- **Turning hooks off for one session.** During test-first work you will sometimes
  want a failing test on purpose, and the Stop hook will keep nudging Claude to fix
  it. Start that session with hooks off; your files are not changed:

  ```bash
  claude --settings '{"disableAllHooks": true}'
  ```

- **The deny rules are not a sandbox.** They stop Claude's Read, Grep and Glob tools
  and the file commands Claude Code recognises in Bash, such as `cat .env`. They do
  not stop a Python or Node script, or `grep -r` run in that folder, from opening the
  file. Keep real secrets out of the project folder, or turn on Claude Code's
  sandbox for OS-level blocking.
- **The lint hook only sees Claude's Edit and Write tools.** A file rewritten by a
  Bash command does not trigger it. The Stop hook still runs the tests.
- **A project with no tests yet** is not blocked: pytest's "no tests collected" counts
  as a pass.

## Testing the hooks

The guide repository tests these scripts against a throwaway uv project. From the
repository root:

```bash
uv run --with pytest pytest tools/tests/test_hooks.py
```
