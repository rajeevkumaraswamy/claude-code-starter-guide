# Session 5: Review and team baseline

About 2 hours, plus about 15 minutes of GitHub setup that you do first (next
block). Take a break after section 4 if you like: your work waits on its branch.
By the end `sensorlog` can plot a sensor and has a command,
`sensorlog summary <csv>`, both built test first on a branch. You have reviewed
the change yourself and with `/code-review`, pushed it to your own private GitHub
repository and opened a pull request. You have also switched the project to the
team baseline, so you know every line of the setup you will copy into the real
project.

Before you start: Session 4 is committed, and in `practice/` the command
`uv run pytest checkpoints/test_session_5.py` fails with
`ModuleNotFoundError: No module named 'sensorlog.plot'`.

As before, keep two terminals open: Claude in one, and in the other your own
checks, after `cd ~/claude-code-starter-guide/practice`.

## Before Session 5: your own GitHub repository (about 15 minutes, once)

**Why:** a pull request needs a GitHub repository you can push to. You make a
**private copy of your clone** under your own account. Don't fork the guide
repository: a fork made on GitHub copies only the default branch unless you
change an option, so you would lose the `reference` branch.

All of this happens in your normal terminal, not inside Claude. In the commands
below, replace `<you>` with your GitHub username.

1. **Install and log in to the GitHub CLI** (skip what you already have):

   ```bash
   gh --version || sudo apt install -y gh
   gh auth login
   ```

   At the `gh auth login` questions choose **GitHub.com**, **HTTPS**, **Yes** to
   authenticate Git with your GitHub credentials, and **Login with a web
   browser**. Check:

   ```bash
   gh auth status
   ```

   Pass: a line saying you are logged in to `github.com`, with your username.

2. **Make sure everything is committed** and you are on `main`, from the
   repository root:

   ```bash
   cd ~/claude-code-starter-guide
   git status
   git branch --show-current
   ```

   Pass: `nothing to commit` (untracked files are fine), and `main`. If you have
   changes, commit them first.

3. **Create the repository and push `main` to it.** Your clone's `origin`
   currently points at the guide repository. Rename it to `upstream` (so you can
   still pull guide updates), then create your private repository as the new
   `origin`:

   ```bash
   git remote rename origin upstream
   gh repo create claude-code-practice --private --source . --remote origin --push
   ```

   `--source .` uses this clone, `--push` pushes the branch you are on (`main`).
   Your local `reference` branch stays as it is; you don't need to push it.

4. **Tell `gh` which repository is yours.** The clone now has two GitHub
   remotes, so `gh pr ...` commands could ask which one to use, or pick the guide
   repository. Set your own as the default:

   ```bash
   gh repo set-default <you>/claude-code-practice
   gh repo set-default --view
   ```

   Pass: the second command prints `<you>/claude-code-practice`.

5. **Record origin's default branch.** `/security-review` (section 5) compares
   your branch with it and fails with `ambiguous argument 'origin/HEAD...'`
   without this:

   ```bash
   git fetch origin
   git remote set-head origin --auto
   git symbolic-ref refs/remotes/origin/HEAD
   ```

   Pass: the last command prints `refs/remotes/origin/main`. Then:

   ```bash
   git remote -v
   ```

   Pass: `origin` points at `github.com/<you>/claude-code-practice`, and
   `upstream` at the guide repository.

## 1. A branch and the `sensorlog` command

**Why:** work for review lives on its own branch, so `main` stays the known-good
version and the pull request shows exactly this change.

```bash
cd ~/claude-code-starter-guide/practice
git switch -c feat/plot-and-cli
```

A command such as `sensorlog` is declared in `pyproject.toml`. The line below
says "`sensorlog` runs the function `main` in the module `sensorlog.cli`".
Add it by hand: this is project configuration, so you decide it, not Claude.
From `practice/`, append it to the end of the file:

```bash
cat >> pyproject.toml <<'EOF'

[project.scripts]
sensorlog = "sensorlog.cli:main"
EOF
```

Then install the command into the project's environment and try it:

```bash
uv sync
uv run sensorlog summary data/sample.csv
```

Pass: `uv sync` finishes without an error, and `uv run sensorlog` fails with
`ModuleNotFoundError: No module named 'sensorlog.cli'`. The command exists now;
the code behind it doesn't, yet.

## 2. Test first: `plot_sensor` and the command

Same two prompts as Session 4: Prompt 1 with hooks off, so you can see red;
Prompt 2 with hooks on.

**Prompt 1, with hooks off.** In your Claude terminal, from `practice/`:

```bash
claude --settings '{"disableAllHooks": true}'
```

```text
Write failing tests for these two features per the spec; do not implement
yet. Put them in tests/test_plot.py and tests/test_cli.py.

Spec 1, a new module src/sensorlog/plot.py:
plot_sensor(df, sensor_id: str, out_path: Path) -> Path
- df has the columns load_csv returns (timestamp, sensor_id, value).
- Writes a PNG line plot of that sensor's values over time to out_path and
  returns out_path.
- Raises ValueError if sensor_id does not appear in df.
- Must work on a machine with no display.

Spec 2, a new module src/sensorlog/cli.py with main(argv=None) -> int, run
as the command `uv run sensorlog summary <csv>` (already declared in
pyproject.toml):
- Loads the CSV with load_csv and prints one line per sensor, sorted by
  sensor_id, formatted
  "{id}: count={n} mean={m:.3f} min={lo:.3f} max={hi:.3f}"
  using summarize from sensorlog.stats.
- If the file does not exist: prints an error message to stderr and exits
  with code 2.
```

Run the new tests yourself, in your second terminal:

```bash
uv run pytest tests/test_plot.py tests/test_cli.py
```

**Red.** Pass: either a `ModuleNotFoundError` naming `sensorlog.plot` or
`sensorlog.cli` while collecting a test file (then no test in that file runs,
which is expected), or the tests run and fail; for tests that run the command,
the output shows `ModuleNotFoundError`. A typo or a broken test is the wrong
reason: ask Claude to fix the test, and run it again.

Leave this session with `/exit`, then freeze the tests:

```bash
git add tests/test_plot.py tests/test_cli.py
```

Check the new tests are tidy (the lint hook was off while Claude wrote them):
run `uv run ruff check .`. If it flags anything in `tests/`, run
`uv run ruff format tests` and `uv run ruff check --fix tests`, then `git add`
the test files again.

**Prompt 2, hooks back on.**

```bash
claude
```

```text
Implement src/sensorlog/plot.py and src/sensorlog/cli.py until
tests/test_plot.py and tests/test_cli.py pass. Do not modify the tests.
Run uv run pytest and show me the output.
```

Then check, in your second terminal:

```bash
uv run pytest
git diff tests/
uv run pytest checkpoints/test_session_5.py
uv run sensorlog summary data/sample.csv
```

**Green.** Pass: no failures; `git diff tests/` prints **nothing**; the
checkpoint ends with `4 passed`; and the command prints three lines, starting
`pressure_1: count=120 mean=`, then `temp_1:` and `temp_2:`.

Stay in this Claude session for the next two sections.

## 3. Review the diff yourself

**Why:** you are the first reviewer of anything Claude writes. Hooks and tests
catch what you thought to check; reading the diff catches the rest: code you
didn't ask for, a new dependency, a quiet change to something unrelated.

Stage everything for this change and read it, in your second terminal:

```bash
git add src tests pyproject.toml
git status
git diff --staged --stat
git diff --staged
```

(`git diff` on its own leaves out new files Git doesn't track yet; staging them
first and using `--staged` shows everything you are about to commit.)

Pass: `git status` lists only `pyproject.toml` and new or changed files under
`src/sensorlog/` and `tests/`. Nothing under `checkpoints/`, and no `uv.lock`
change (no new dependency). If something else changed, ask Claude why before
you go on.

Read the code with these questions:

- Does it do anything the spec didn't ask for?
- Where does an error go: stdout, stderr, or an exception with a long traceback?
- Is anything imported that isn't in `pyproject.toml`?

Then ask Claude for the failure cases you didn't think of:

```text
Look at the staged changes (git diff --staged). What could break? List the
five most likely ways plot_sensor or the sensorlog command fails on real
inputs, most likely first, and say for each whether a test covers it. Don't
change anything.
```

Typical answers: an empty CSV, a CSV with the wrong columns, an output folder
that doesn't exist, a sensor with only NaN values. You don't have to fix them
all now. Optional, if you have time: choose one that matters, and fix it the
usual way, a failing test first, then the code.

## 4. `/code-review`

**Why:** a second reader with fresh context. `/code-review` is built into Claude
Code (`/review` does the same). It runs as a subagent with its own context
window, looks for correctness bugs, and reports its findings into your
conversation.

```text
/code-review
```

With no target it reviews your branch's changes against `main`, including
staged and uncommitted work. It runs in the background; keep reading while it
works. The findings arrive as a message in your conversation, each with a file
location and a short explanation.

For each finding, decide:

- **A real bug:** ask Claude to fix it test first ("Write a failing test for
  this finding, show me it fail, then fix the code").
- **Not a problem here, or a matter of taste:** skip it. A reviewer, human or
  not, can be wrong.

Two options worth knowing: `/code-review high` reviews more widely and reports
more (and less certain) findings, and later plain `/code-review` runs reuse the
level you typed last (`/code-review medium` sets it back); `/code-review --fix` applies the findings
itself. Skip `--fix` while you learn: you want to see each finding before any
code changes, and its edits are not undone by `/rewind`. The review uses your
plan's usage, like any other prompt.

If you changed anything, run `uv run pytest` again and re-stage with
`git add src tests`.

## 5. Commit, push, open a pull request

```bash
git add src tests pyproject.toml
git commit -m "feat: plot_sensor and sensorlog summary command"
git push -u origin HEAD
gh pr create --fill
```

`git push -u origin HEAD` pushes the current branch to your repository under the
same name. `gh pr create --fill` opens a pull request against `main`, using your
commit message as its title and description. It prints the pull request's URL.

**Security review.** Now that the branch is pushed, in Claude:

```text
/security-review
```

It checks the changes on your branch against `origin`'s default branch for risks
such as injection or exposed secrets. For this change it will probably find
little; on a real project, run it before you ask someone else to review. If it
fails with `ambiguous argument 'origin/HEAD...'`, redo step 5 of "Before Session 5".

**Review the pull request.** This is how you review anyone's pull request. In
your second terminal:

```bash
gh pr view
gh pr diff
```

`gh pr view` shows the title, description, state and checks; `gh pr diff` shows
the change. Leave a review comment:

```bash
gh pr comment --body "Reviewed: plot and CLI match the spec; tests seen red then green."
```

You can also ask Claude to review it. The team settings already allow Claude to
run `gh pr view` and `gh pr diff` without asking:

```text
Review the open pull request on this branch using gh pr view and gh pr diff.
List anything you would ask the author to change, with file and line.
```

**A teammate's pull request.** If a teammate adds you to their repository
(GitHub, **Settings**, **Collaborators**), list and read their pull requests with
`gh pr list --repo <owner>/claude-code-practice`, then
`gh pr diff <number> --repo <owner>/claude-code-practice`. Leave your review with
`gh pr review <number> --repo <owner>/claude-code-practice --comment --body "..."`
(or `--approve`). GitHub doesn't let you approve your own pull request, which
is why you used a comment above.

## 6. Adopt the team baseline

**Why:** so far the `CLAUDE.md` in `practice/` is the one you wrote in Session 1,
and its `.claude/` folder is the team's (copied in Session 3). The real project will
start from the shipped team baseline in `baseline/`, so everyone gets the same
rules. Here you read every line of it, then switch this project to it, exactly as
you will in the real project.

### `baseline/CLAUDE.md`, line by line

Open it alongside this text (`cat ../baseline/CLAUDE.md` from `practice/`).

| Section | What it says | Why it is there |
| :- | :- | :- |
| **Commands** | How to test, lint, format and run one test | Claude doesn't have to guess or search; these are also the commands the hooks use. |
| (paragraph under Commands) | Hooks already run ruff and the tests; treat their messages as real failures | So Claude doesn't argue with the hooks or "work around" them. |
| **How to work here**: failing test first | Write or update a failing test, show it fail, then change the code | Sessions 2 to 5 in one line. |
| Show test output before claiming done | Paste the `uv run pytest -q` summary line | Evidence, not a summary. |
| Never weaken or delete a test | Ask first; if a test looks wrong, say why and wait | Stops "make the tests pass" by editing the tests. |
| No new dependencies without asking | Includes `uv add` and imports of packages not in `pyproject.toml` | Dependencies are a team decision. |
| Keep changes small | Mention other problems instead of fixing them unasked | Keeps every diff reviewable. |
| Don't read `.env` or `secrets/` | Advice, backed by deny rules in `settings.json` | `CLAUDE.md` asks; settings enforce. |
| **This project** | Placeholders: what it does, where code and tests live, Python version, data, never touch, conventions, ask before | The only part you write. Everything Claude can't discover from the code. |

### `baseline/.claude/settings.json`, line by line

Open it (`cat .claude/settings.json` from `practice/`; it is the same file).

| Line | What it does |
| :- | :- |
| `"$schema": ...` | Lets your editor check and autocomplete the file. No effect on Claude Code. |
| `"Bash(uv run pytest *)"`, `"Bash(uv run ruff *)"` | Claude may run the tests and ruff without asking. Safe, and you want them run often. |
| `"Bash(git status *)"`, `"Bash(git diff *)"`, `"Bash(git log *)"` | Read-only git, without asking. `git commit` and `git push` still ask. |
| `"Bash(gh pr view *)"`, `"Bash(gh pr diff *)"` | Read a pull request without asking; you saw this in section 5. |
| `"deny"`: `Read(**/.env)`, `Read(**/.env.*)`, `Read(**/secrets/**)` | Claude's file tools may not read these. Not a sandbox: a script Claude runs can still open them, so keep real secrets out of the project folder. |
| `"PostToolUse"` with `"matcher": "Edit\|Write"` | After every Edit or Write, run `lint-after-edit.sh` (ruff fix and format). `"timeout": 120` is in seconds. |
| `"Stop"` | When Claude tries to finish, run `tests-before-stop.sh` (the test suite), with up to 600 seconds. |
| `"$CLAUDE_PROJECT_DIR"` | The project root, so the hooks are found from any folder Claude is in. |

Everything not in the allow list still asks you. `baseline/README.md` lists the
same points, plus what to know when you install it elsewhere.

**What you may need to change in the real project:**

- **Slow tests.** The Stop hook runs the whole suite every time Claude finishes.
  If that takes minutes (simulations, training runs), mark the slow tests with a
  pytest marker and change the hook's `uv run --quiet pytest -q` to
  `uv run --quiet pytest -q -m "not slow"`. Run the slow ones yourself.
- **Different commands.** If the project isn't uv + pytest + ruff, change the
  Commands section, the allow rules and both hook scripts together.
- **More allow rules** only for commands that can't do damage. Never `git push`,
  `rm` or a blanket `Bash`.

### Switch `practice/` to the baseline

1. **Keep what's worth keeping.** Read your Session 1 file, and note any line the
   baseline doesn't cover (at least "Never edit files in checkpoints/"):

   ```bash
   cat CLAUDE.md
   ```

2. **Replace it** with the team file, from `practice/`:

   ```bash
   cp ../baseline/CLAUDE.md CLAUDE.md
   nano CLAUDE.md
   ```

3. **Fill in "This project".** Replace every `<...>` placeholder and delete the
   `<!-- Fill in ... -->` comment line. For this project, for example:

   ```markdown
   - What it does: sensorlog, a small toolkit to load, clean, summarise and plot sensor CSV logs.
   - Code lives in: src/sensorlog/
   - Tests live in: tests/
   - Python version: 3.12
   - Data or fixtures: data/sample.csv (clean) and data/messy.csv (duplicates, gaps, out-of-order rows)
   - Never touch: checkpoints/ (the guide's acceptance tests), uv.lock by hand
   - Conventions: type hints on public functions; functions return new DataFrames and never modify their input
   - Ask before: changing a public function's signature
   ```

   Save with `Ctrl+O`, `Enter`, then leave nano with `Ctrl+X`. Check that no
   placeholder is left:

   ```bash
   grep -n '<' CLAUDE.md || echo "no placeholders left"
   ```

   Pass: `no placeholders left`.

4. **Check Claude reads it.** Leave Claude with `/exit`, start `claude` again in
   `practice/`, and ask:

   ```text
   Which files must you never change in this project, and what must you show
   me before saying a task is done?
   ```

   Pass: Claude names `checkpoints/`, and the `uv run pytest -q` summary line.

5. **Commit it to the branch and push.** The pull request picks up the new
   commit:

   ```bash
   git add CLAUDE.md
   git commit -m "chore: adopt team baseline CLAUDE.md"
   git push
   gh pr view --json commits --jq '.commits | length'
   ```

   Pass: the last command prints `2` (or more, if you committed review fixes
   separately).

### In the real project later

Follow the Install steps in `baseline/README.md`: copy `baseline/CLAUDE.md` and
`baseline/.claude/` into the project root, merge by hand if the project already
has a `.claude/settings.json`, fill in "This project", commit both, then start
`claude`, accept the trust prompt, and check `/hooks` lists both hooks. Keep the
team's copy in one place (this repository's `baseline/`), and propose changes to
it by pull request, so everyone stays on the same version.

## 7. Where next

You have used only what ships with Claude Code. That's deliberate: these are the
habits everything else builds on. When you want more:

- **Plugins** add commands, skills, subagents and hooks. Run `/plugin` to browse
  the **Discover** tab of Anthropic's official marketplace. One example is
  **superpowers**, a collection of workflow skills (brainstorming, planning,
  test-driven development, reviews) that enforce much of what this guide asks
  you to do by hand. Install plugins one at a time, read what each adds, and
  agree team-wide plugins together, as you did with the baseline.
- **Second-opinion tools.** Some teams ask a different AI tool, such as OpenAI's
  Codex, to review Claude's work. This team doesn't have Codex access. Use
  `/code-review`, `/security-review` and a human reviewer.
- **The next guide** applies these habits to model predictive control and
  reinforcement learning work: simulations, longer-running tests and research
  papers.

Optional, when you are done with the pull request: merge it with
`gh pr merge --squash --delete-branch`, then `git switch main` and `git pull`.
To delete the practice repository later, run
`gh repo delete claude-code-practice --yes`. It needs an extra permission on your
login first: `gh auth refresh -s delete_repo`.

## Checkpoint

From `practice/`, in a normal terminal:

```bash
uv run pytest checkpoints/test_session_5.py
uv run pytest
git status checkpoints/
uv run sensorlog summary data/sample.csv
gh pr list
grep -n '<' CLAUDE.md || echo "no placeholders left"
```

| Command | Pass |
| :- | :- |
| `uv run pytest checkpoints/test_session_5.py` | Ends with `4 passed` |
| `uv run pytest` | No failures, and includes `tests/test_plot.py` and `tests/test_cli.py` |
| `git status checkpoints/` | Shows no changes |
| `uv run sensorlog summary data/sample.csv` | Three lines: `pressure_1: ...`, `temp_1: ...`, `temp_2: ...` |
| `gh pr list` | Lists your pull request from `feat/plot-and-cli` (if you merged it, `gh pr list --state merged`) |
| `grep ... CLAUDE.md` | `no placeholders left` |

Stuck? From the repository root:
`git show reference:practice/src/sensorlog/cli.py` (or `plot.py`, or
`git show reference:practice/pyproject.toml`).

## Why it matters

Tests show the code does what you specified; review shows it does nothing else.
Read the diff yourself first, then use `/code-review` as a second reader, then a
pull request so a teammate can see the same change. The baseline puts all of
this into files you commit: `CLAUDE.md` for the habits, `settings.json` and hooks
for the checks, so the real project starts with them from the first prompt.

That's the guide. Keep [Appendix B](appendix-b-cheat-sheet.md) open while you
work, and [Appendix C](appendix-c-troubleshooting.md) for when something goes
wrong.
