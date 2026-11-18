# Session 0: Setup

About 60 to 75 minutes. By the end Claude Code is installed, logged in to your Max
plan and healthy; the practice project's tests run; you have had a first
conversation; and you know which permission mode, model, effort level and how
much usage you are on.

New to the terminal? Do [Appendix A](appendix-a-linux-primer.md) first.

You should already have cloned this repository into `~/claude-code-starter-guide`
(see the README). Check:

```bash
ls ~/claude-code-starter-guide/practice
```

You should see `checkpoints  data  exercises  pyproject.toml  README.md  src  tests  uv.lock`.

## 1. Install or update Claude Code

**Why:** an old install, two installs side by side, or old personal settings are
the most common causes of "it doesn't do what the guide says".

Take **Path A** if `claude --version` prints `command not found`. Take **Path B**
if it prints a version.

### Path A: fresh install

1. Install with the official native installer. It needs no `sudo` and updates itself
   in the background:

   ```bash
   curl -fsSL https://claude.ai/install.sh | bash
   ```

   It shows no progress while it downloads. Wait for the prompt to come back.

2. **Open a new terminal window** (the old one does not know about the new
   command yet), then:

   ```bash
   claude --version
   ```

   Pass: a version number followed by `(Claude Code)`, for example
   `2.1.327 (Claude Code)`.

   If it says `command not found`, the install folder `~/.local/bin` is not on your
   PATH. Fix it once:

   ```bash
   echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
   source ~/.bashrc
   ```

3. Check the installation:

   ```bash
   claude doctor
   ```

   `claude doctor` is read-only: it prints diagnostics and changes nothing. Pass: a
   `Running: native (...)` line, `Auto-updates: enabled`, and
   `No installation issues found.` near the end.

You log in in section 3 below. Skip to [2. Python toolchain](#2-python-toolchain).

### Path B: already installed

1. **Find every copy.** More than one install causes version mix-ups:

   ```bash
   which -a claude
   ```

   Pass: exactly one line, `/home/<you>/.local/bin/claude` (the native install).

   If you see anything else (an npm install, or a second path):
   - Install the native version with the Path A command and open a new terminal.
   - Remove the npm copy: `npm uninstall -g @anthropic-ai/claude-code`
   - Run `which -a claude` again until only the `~/.local/bin/claude` line is left.

2. **Update and check:**

   ```bash
   claude update
   claude --version
   claude doctor
   ```

   Pass: `claude update` ends with `to version <x>` or
   `Claude Code is up to date (<x>)`; `claude doctor` ends with
   `No installation issues found.` If `claude doctor` lists settings errors, fix
   or move the file it names (next step).

3. **Look for leftovers that would fight the team setup.** Claude Code reads your
   personal settings and instructions in every project, on top of the project's.
   Look at both files (a `No such file or directory` error just means you have
   none, which is fine):

   ```bash
   cat ~/.claude/settings.json
   cat ~/.claude/CLAUDE.md
   ```

   These get in the way of this guide:

   | In `~/.claude/settings.json` | Why it gets in the way |
   | :- | :- |
   | `"defaultMode"` set to `"bypassPermissions"` or `"acceptEdits"` | You will not see the prompts this session teaches |
   | `"disableAllHooks": true` | The automatic lint and test checks in Session 3 never run |
   | A `"hooks"` block | Your personal hooks run alongside the team hooks in every project |
   | Very broad `"allow"` rules, such as `"Bash"` or `"Bash(*)"` | Claude runs any command without asking |
   | `"model"` or `"effortLevel"` | The model and effort steps below will not match |

   In `~/.claude/CLAUDE.md`, look for instructions that contradict test-first work,
   such as "skip tests", "don't write tests", "commit automatically" or "never ask
   me". Every `CLAUDE.md` Claude finds is loaded together, so these mix with the
   project's instructions.

   If you find any of these, move the file aside for the week rather than editing
   it. Moving keeps it, so you can put it back later. Your login is stored
   elsewhere and is not affected:

   ```bash
   mv ~/.claude/settings.json ~/.claude/settings.json.bak
   mv ~/.claude/CLAUDE.md ~/.claude/CLAUDE.md.bak
   ```

   Then run `claude doctor` again.

## 2. Python toolchain

**Why:** the practice project and the team baseline both use
[uv](https://docs.astral.sh/uv/). It installs Python 3.12 for you without `sudo`,
creates the project's virtual environment and runs commands inside it. This
section is the only place the guide installs Python tools; everywhere else you
just run `uv run <command>`.

1. Install uv (skip if `uv --version` already prints a version):

   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

   Open a new terminal, then check: `uv --version` prints `uv` and a version number.

2. Install Python 3.12 and the project's dependencies:

   ```bash
   uv python install 3.12
   cd ~/claude-code-starter-guide/practice
   uv sync
   ```

   `uv sync` creates `practice/.venv` and installs pandas, matplotlib, pytest and
   ruff. It ends with a line like `Installed 18 packages` (or `Audited ...` if
   they were already there).

3. Run the project's tests:

   ```bash
   uv run pytest
   ```

   Pass: the last line reads `6 passed`.

## 3. First run and login

**Why:** your first session sets up the login and asks whether you trust the
folder. You also want to start in the mode where Claude asks before it does
anything, so you see what it is about to do.

1. Start Claude Code **inside `practice/`**, in Manual mode:

   ```bash
   cd ~/claude-code-starter-guide/practice
   claude --permission-mode default
   ```

   (Why the flag: recent versions start new sessions in auto mode, where a second
   model approves actions for you instead of asking. Section 4 explains this.)

2. Follow the prompts:
   - Pick a theme.
   - Log in with your **Claude account** (the one with the Max plan). A browser
     opens; sign in and approve. If no browser opens, for example over SSH, press
     `c` at the login prompt to copy the URL, open it on any machine, sign in, and
     paste the code it shows at the `Paste code here` prompt.
   - Claude Code asks whether you trust this folder. It is the guide repository
     you just cloned, so accept. Trust matters later: Claude Code does not run a
     project's hooks, or apply its `allow` rules, until you have accepted.

3. Check what you are logged in as. Type this and press Enter:

   ```text
   /status
   ```

   Pass: the Status tab shows your account and the model. Press `Esc` to close it.
   Look at the bottom of the screen: the status bar shows `manual mode on`.

You only log in once. To switch accounts later, run `/login` inside a session.
To leave Claude Code, type `/exit` (or press `Ctrl+D` twice).

## 4. Permission modes

**Why:** the permission mode decides what Claude may do without asking you. While
you learn, you want to see each file edit and each command before it happens.

| Mode | Status bar | What Claude does without asking | Use it for |
| :- | :- | :- | :- |
| Manual (`default`) | `manual mode on` | Read files | Learning; anything sensitive. **Use this for the whole guide.** |
| Accept edits (`acceptEdits`) | `accept edits on` | Read and edit files, plus simple file commands like `mkdir` and `mv` | Iterating on code you are reviewing as it changes |
| Plan (`plan`) | `plan mode on` | Read and explore only; proposes a plan instead of changing files | Thinking before coding (Session 1) |
| Auto (`auto`) | `auto mode on` | Almost everything; a separate model reviews each action and blocks risky ones | Long tasks once you trust your setup |

- `Shift+Tab` cycles the mode in a running session: Manual, then accept edits, then
  plan, then back round (auto is also in the cycle when available).
- Since v2.1.283, new interactive sessions start in **auto** unless you say
  otherwise. Auto is useful, but it hides the very thing you need to learn now:
  what Claude is about to do. Opt into it after the guide, once you know what you
  would have approved.

**Make Manual your starting mode for the rest of the guide**, so a plain `claude`
starts the same way. This adds one setting to your personal settings file and keeps
anything else already in it (it prints the file when done):

```bash
python3 - <<'EOF'
import json, pathlib
p = pathlib.Path.home() / ".claude" / "settings.json"
p.parent.mkdir(exist_ok=True)
data = json.loads(p.read_text()) if p.exists() else {}
data.setdefault("permissions", {})["defaultMode"] = "default"
p.write_text(json.dumps(data, indent=2) + "\n")
print(p.read_text())
EOF
```

Pass: the output contains `"defaultMode": "default"`. (If it prints a
`JSONDecodeError` instead, your existing file is not valid JSON: open it with
`nano ~/.claude/settings.json` and fix it, or move it aside as in Path B.) To go
back to auto later, delete that line from the file.

**Permission prompts.** When Claude wants to edit a file or run a command, it stops
and asks. You will usually get three kinds of answer:

- **Yes**: allow this one action.
- **Yes, and don't ask again** for this kind of command: Claude Code saves an `allow`
  rule in `.claude/settings.local.json` in this repository (kept out of git). Use it
  only for commands that cannot do damage, such as running the tests.
- **No**: refuse, and tell Claude what to do instead.

Read the command before you answer. For now, prefer plain **Yes**.

## 5. First conversation

**Why:** asking Claude to explain an unfamiliar project is the safest useful thing
it can do: it only reads. Then you see your first permission prompt.

Start Claude in `practice/` (now just `claude`, since Manual is your default) and
check that the status bar shows `manual mode on`. Then type:

```text
Explain this project to me: what each module in src/sensorlog does, what the
data in data/ looks like, and how the tests are organised. Keep it short.
```

Claude reads files without asking. Its answer will differ from anyone else's;
that is fine.

Now ask it to do something that needs permission:

```text
Run the test suite and tell me how many tests passed.
```

Claude asks before it runs `uv run pytest`. Read the command it shows, then choose
**Yes**. Compare its answer with what you saw yourself in section 2. They should
match: this is the habit for the whole guide. You trust the test output, not the
summary.

While Claude is working, `Esc` stops it. Nothing it already did is lost.

## 6. Model and effort

**Why:** the model decides how capable Claude is; the effort level decides how long
it thinks before answering. Both affect quality, speed and how fast you use up your
plan.

On a Max plan the default model is Opus 5.5 at `medium` effort. Look at them:

```text
/model
```

The picker shows the models and marks the current one. Press `Esc` to leave it
unchanged. (Choosing a model there with `Enter` saves it as your default for new
sessions.)

```text
/effort status
```

Prints the current effort level.

**Recommendation:**

- **Leave the model on the default.** Do not switch around while learning; it makes
  results harder to compare.
- **Raise effort for planning and debugging**, not for routine edits:
  - For one hard question, put the word `ultrathink` anywhere in your prompt. It
    applies to that one turn only.
  - For a longer stretch of planning or debugging, run `/effort high`. This is
    **saved as your default**, so when you are done run `/effort auto` to go back
    to the model's default.
- Phrases like "think hard" or "think more" are not special any more. Claude Code
  treats them as normal words. Use `ultrathink` or `/effort`.

## 7. Usage on Max 5x

**Why:** Max is a fixed monthly plan, not pay-per-token, but it has usage limits.
Long sessions, high effort and many parallel helpers use them up faster.

```text
/usage
```

On a Max plan this shows your plan usage bars, activity stats, and a breakdown of
what is using your limit with suggestions. Ignore the dollar "session cost" figure:
it is computed for API users and is not what you pay.

What it means in practice:

- Limits are counted in a session window and a weekly window. When you hit one,
  Claude Code tells you which and when it resets.
- The Claude Code docs do not publish fixed numbers for Max 5x, and they change.
  Do not plan around a number; check `/usage` instead.
- A normal day of this guide should not get near the limit. If it does, the usual
  causes are one very long conversation (Session 1 teaches `/clear` and
  `/compact`) or leaving effort on `high` or `max`.
- Check `/usage` at the start and end of each session for the first week. You
  will quickly learn what a "normal" session costs you.

Leave Claude Code with `/exit`.

## Checkpoint

Run these in a normal terminal (not inside Claude Code):

```bash
claude --version
cd ~/claude-code-starter-guide/practice
uv run pytest
uv run pytest checkpoints/test_session_1.py
```

| Command | Pass |
| :- | :- |
| `claude --version` | Prints a version number followed by `(Claude Code)` |
| `uv run pytest` | Last line reads `6 passed` |
| `uv run pytest checkpoints/test_session_1.py` | **Fails** with `ImportError: cannot import name 'summarize' from 'sensorlog.stats'` and `1 error`. This is expected: red now, green after Session 1. |

Also confirm, in your personal settings, that new sessions start in Manual:

```bash
grep defaultMode ~/.claude/settings.json
```

Pass: `"defaultMode": "default"`.

If something does not pass, see "Getting unstuck" in the README, and Appendix C
(common problems).

## Why it matters

Everything after this assumes three things: one healthy, current install with no
leftover settings working against you; a test command you have run yourself and
can trust; and a mode where Claude asks before it acts. Later sessions take those
for granted. When something looks wrong, these are the first three things to check.

Next: Session 1, Working with Claude (`01-working-with-claude.md`).
