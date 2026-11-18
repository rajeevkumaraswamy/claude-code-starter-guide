# Appendix B: Cheat sheet

Every command, key and slash command the guide uses, grouped by the session that
introduces it. Slash commands and keys are typed **inside Claude Code**; the rest
in your shell (run checks in your second terminal, in `practice/`). For terminal
basics (`cd`, `ls`, `cat`, `Ctrl+C`), see [Appendix A](appendix-a-linux-primer.md).

## Session 0: Setup

| Shell | What it does |
| :- | :- |
| `curl -fsSL https://claude.ai/install.sh \| bash` | Install Claude Code (native installer) |
| `claude --version` / `claude update` / `claude doctor` | Show version / update now / check the install (read-only) |
| `which -a claude` | List every `claude` on your PATH (want exactly one) |
| `claude --permission-mode default` | Start one session in Manual mode |
| `curl -LsSf https://astral.sh/uv/install.sh \| sh` | Install uv |
| `uv python install 3.12`, `uv sync` | Install Python 3.12; install the project's dependencies |
| `uv run pytest` | Run the project's tests (`tests/`) |

| In Claude | What it does |
| :- | :- |
| `/status` | Account, model, settings sources (`Esc` closes it) |
| `/login` / `/exit` (or `Ctrl+D` twice) | Log in / leave Claude Code |
| `Shift+Tab` | Cycle permission mode: Manual, accept edits, plan |
| `Esc` | Stop Claude (keeps what it did) or close a dialog |
| `/model` | Show or pick the model (`Esc` leaves it unchanged) |
| `/effort status`, `/effort high`, `/effort auto` | Show effort; raise it (saved); back to default |
| `ultrathink` (in a prompt) | Think harder for that one turn |
| `/usage` | Plan usage and reset times |

## Session 1: Working with Claude

| In Claude | What it does |
| :- | :- |
| `@` + path | Put a file into the conversation |
| Plan approval | **Yes, manually approve edits** / **No, keep planning** (`Esc` to leave; `Shift+Tab` there approves) |
| `/rewind` (or `Esc` twice, empty prompt) | Go back to before a prompt: **Restore code and conversation** |
| `/context` | How full the context window is |
| `/clear` | New conversation (new task) |
| `/compact` (optionally with what to keep) | Summarise and continue (same task, long conversation) |
| `/init`, `/memory` | Draft a project `CLAUDE.md`; open it for editing |

| Shell | What it does |
| :- | :- |
| `claude` (in `practice/`) | Start Claude Code |
| `uv run pytest checkpoints/test_session_<N>.py` | Run session N's checkpoint on its own |
| `nano CLAUDE.md` | Edit a file: `Ctrl+O` then `Enter` saves, `Ctrl+X` quits |
| `git add ...` then `git commit -m "..."` | Commit your work (don't `git push` to the guide's `origin`) |

## Session 2: Test-first features

| Shell | What it does |
| :- | :- |
| `uv run pytest tests/test_clean.py` | Run one test file (red, then green) |
| `git add tests/test_clean.py` | Freeze the tests after you've seen them fail |
| `git diff tests/` | After green: must print nothing (tests unchanged) |
| `git restore src/sensorlog/clean.py` | Throw away uncommitted changes to a file |
| `git status checkpoints/` | Checkpoints untouched? |

Prompts: "Write failing tests for X per this spec; do not implement yet." then
"Implement X until the tests pass. Do not modify the tests."

## Session 3: Debugging and automatic checks

| | What it does |
| :- | :- |
| `uv run pytest checkpoints/test_session_3.py` | Run one checkpoint on its own |
| `uv run ruff check .` | Lint everything |
| `cp -R baseline/.claude practice/` (repo root) | Install the team hooks and settings |
| `/hooks` | List active hooks (want `PostToolUse` and `Stop`) |
| `claude --settings '{"disableAllHooks": true}'` | One session with all hooks off |

Rule: say "Fix the code so this test passes. Do not modify the tests.", never
"make the tests pass". Ask for "the pytest output", not a summary.

## Session 4: Research

| | What it does |
| :- | :- |
| WebSearch / WebFetch prompts | **Yes** (once), **Yes, and don't ask again for** a domain, **No** |
| `Ctrl+F` in the browser | Find Claude's quote on the source page |
| "Use a subagent to ..." | Side task in its own context; only the summary comes back |
| `claude --settings '{"disableAllHooks": true}'`, then `/exit`, `git add tests/...`, `claude` | Red step with hooks off, green step with hooks on |
| `uv run ruff format tests`, `uv run ruff check --fix tests` | Tidy the tests Claude wrote with hooks off, then `git add` them again |

## Session 5: Review and team baseline

| Shell | What it does |
| :- | :- |
| `gh auth login`, `gh auth status` | Log in to GitHub; check |
| `git remote rename origin upstream` | Keep the guide repository as `upstream` |
| `gh repo create <name> --private --source . --remote origin --push` | Private copy of your clone, `main` pushed |
| `gh repo set-default <you>/<name>`, `gh repo set-default --view` | Make `gh` use your repository, not the guide's; check |
| `git fetch origin`, `git remote set-head origin --auto` | Record origin's default branch (needed by `/security-review`) |
| `git symbolic-ref refs/remotes/origin/HEAD` | Check it: prints `refs/remotes/origin/main` |
| `git remote -v` | Where `origin` and `upstream` point |
| `git switch -c <branch>` | New branch |
| `uv sync`, `uv run sensorlog summary data/sample.csv` | Install the `sensorlog` command; run it |
| `git add ...`, `git diff --staged` | Review exactly what you will commit |
| `git push -u origin HEAD`, `gh pr create --fill` | Push the branch; open a pull request |
| `gh pr view`, `gh pr diff`, `gh pr comment --body "..."` | Read and comment on a pull request |
| `gh pr view --json commits --jq '.commits \| length'` | Count the commits in your pull request |
| `gh pr list`, `gh pr review <n> --comment --body "..."` | List pull requests; review a teammate's |
| `gh pr merge --squash --delete-branch` | Merge (optional) |
| `gh auth refresh -s delete_repo`, `gh repo delete <name> --yes` | Delete the practice repository (optional) |

| In Claude | What it does |
| :- | :- |
| `/code-review` (`/review`) | Background review of your branch for bugs; `high` for more, `--fix` to apply |
| `/security-review` | Security review of your branch against origin's default branch |
| `/plugin` | Browse and install plugins (optional, after the guide) |

## Getting unstuck

| | What it does |
| :- | :- |
| `git show reference:practice/src/sensorlog/<file>.py` | Show the reference solution for a file |
| `git ls-tree --name-only reference practice/src/sensorlog/` | List the reference files |
| `git branch --track reference origin/reference` | Create the local `reference` branch if it's missing |
| `claude --continue` (in `practice/`) | Reopen the last conversation after closing Claude by accident |
| `git restore practice/` (repo root) | Discard all uncommitted changes in `practice/` |
| `/doctor`, `/permissions`, `/logout` | Checkup with fixes; edit saved allow rules; sign out |

Common problems: [Appendix C](appendix-c-troubleshooting.md).
