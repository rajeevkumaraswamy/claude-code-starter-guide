# Session 1: Working with Claude

About 75 to 90 minutes. By the end you have used the loop **explore, then plan,
then build** to add a `summarize` function to `sensorlog`; you can stop Claude
mid-task and undo what it did; you know how to keep a conversation short; and
the project has a `CLAUDE.md` you have edited yourself.

Before you start: Session 0 is done, and in `practice/` the command
`uv run pytest checkpoints/test_session_1.py` fails with
`ImportError: cannot import name 'summarize'`.

Start Claude in `practice/`:

```bash
cd ~/claude-code-starter-guide/practice
claude
```

Check the status bar shows `manual mode on`. (If it shows `auto mode on`, exit and
redo the "Make Manual your starting mode" step in Session 0, section 4.)

**Open a second terminal and keep it open.** Throughout the guide you check
Claude's work by running commands yourself while Claude keeps its conversation.
Open a new terminal window (on Ubuntu, `Ctrl+Alt+T`) and move into the project:

```bash
cd ~/claude-code-starter-guide/practice
```

A new window always starts in your home folder, so do this `cd` every time you
open one; commands like `uv run pytest` only work inside `practice/`. From now
on, "in your second terminal" means this window. Leave it open for every
session. (Don't run these checks by leaving Claude with `/exit`: that ends the
conversation, and later steps build on it.)

## 1. Explore: point Claude at files with `@`

**Why:** Claude does better work when it has read the code it is about to change.
Asking it to explain first costs little, and you find out whether it understood
the project before it touches anything.

Type `@` and then a path relative to `practice/`: Claude Code suggests matching
files as you type. A file you name with `@` is read into the conversation
straight away, so Claude doesn't have to search for it.

Ask:

```text
Explain @src/sensorlog/load.py: what load_csv returns, which columns and
types, and what it does with timestamps. Then look at @data/sample.csv and
tell me which sensors it contains and how often each one is sampled.
```

Read the answer and compare it with the files yourself:

```bash
head -5 data/sample.csv
```

(Run that in your second terminal.)

Pass: Claude's answer matches what you see. The columns are `timestamp`,
`sensor_id` and `value`; there are three sensors (`pressure_1`, `temp_1`,
`temp_2`). If Claude claimed something the files don't show, tell it so. That
is the habit: you check Claude's claims against the files.

## 2. Plan: let Claude think before it edits

**Why:** in plan mode Claude can read and explore but cannot change files. It
proposes a plan and waits. A wrong idea in a plan costs you one sentence to fix;
the same idea in code costs a review, a revert and a re-run.

1. Press `Shift+Tab` until the status bar shows `plan mode on` (twice from
   Manual: Manual, then accept edits, then plan).

2. Give Claude the spec. This is the function the Session 1 checkpoint expects:

   ```text
   Plan a new function in src/sensorlog/stats.py:

   summarize(df) -> dict[str, dict[str, float]]
   - df has the columns load_csv returns.
   - Returns one entry per sensor_id. Each inner dict has exactly the keys
     count, mean, min, max.
   - NaN values are excluded from all four numbers.
   - A sensor whose values are all NaN still appears, with count 0 and NaN for
     mean, min and max.
   - An empty DataFrame returns {}.

   Don't write code yet. Show me the plan.
   ```

3. **Read the plan.** Look for: which file it changes, what it does with NaN,
   whether it plans to change anything you did not ask for (for example
   `load.py`), and whether it says how it will check its work.

4. **Push back on one point.** Every plan can be better; practise saying so.
   When the approval prompt appears, choose **No, keep planning** and type your
   correction. If nothing stands out, use this one:

   ```text
   Don't change load.py or any existing test. After writing the function,
   run uv run pytest checkpoints/test_session_1.py and uv run pytest and
   show me both summary lines.
   ```

   Claude revises the plan and asks again.

5. **Approve.** At the approval prompt choose **Yes, manually approve edits**.
   You go back to Manual mode and approve each edit as it comes.

   The other choice, **Yes, and use auto mode**, lets Claude carry on without
   asking. Not yet.

   **Careful:** at the approval prompt, `Shift+Tab` does not change mode; it
   **approves the plan**. To get out of the prompt without approving, press
   `Esc` first.

## 3. Build it

Claude now writes the code. For each edit it shows the change and asks. Read
each one before you choose **Yes**. When it asks to run `uv run pytest`, read the
command, then allow it.

When Claude says it is done, **don't take its word for it**. Run the checkpoint
yourself, in your second terminal:

```bash
uv run pytest checkpoints/test_session_1.py
uv run pytest
```

Pass: the first ends with `4 passed`; the second has no failures. If the
checkpoint fails, paste the last 20 lines of output to Claude and ask it to
explain the failure before it changes anything.

## 4. Interrupt with `Esc`, undo with rewind

**Why:** sometimes Claude heads off in the wrong direction. Stopping early and
undoing cleanly is cheaper than arguing with a half-finished change.

**Interrupt.** Ask for something long:

```text
Write a detailed docstring for every function in src/sensorlog/.
```

While Claude is working, press `Esc`. It stops. Anything it already did stays
done; nothing is rolled back by `Esc`.

**Rewind.** Now make a change you will throw away:

```text
Rename summarize to summary_stats in src/sensorlog/stats.py.
```

Approve the edits. Then run `/rewind` (or press `Esc` twice with an empty
prompt). The menu lists your prompts. Pick the "Rename summarize..." prompt,
then **Restore code and conversation**. Claude Code puts the files and the
conversation back to how they were before that prompt.

Check that the rename is gone (from `practice/`):

```bash
grep -rn summary_stats src/ || echo "no matches"
uv run pytest checkpoints/test_session_1.py
```

Pass: `no matches`, and the checkpoint still ends with `4 passed`.

If you kept the docstrings from the interrupted prompt, that is fine. To drop
them too, rewind to that prompt instead.

Know the limit: **rewind only restores files Claude changed with its own edit
tools.** A file changed only by a shell command (for example a `sed` or `mv`
that Claude ran) is not restored. Git is your real safety net, so commit at the
end of every session.

## 5. Keep the conversation short: `/clear`, `/context`, `/compact`

**Why:** everything in the conversation is sent to the model on every turn. A
long conversation about old tasks makes Claude slower, uses your plan faster,
and distracts it with details that no longer matter.

```text
/context
```

Shows how full the context window is and what is using it. Run it now and note
the figure.

- **`/clear`** starts a fresh conversation in the same session. Use it **between
  tasks**: you finished `summarize`, so the next task does not need that
  history. Your files are not touched.
- **`/compact`** replaces the conversation so far with a summary and keeps going.
  Use it **in the middle of a long task** when `/context` shows the window
  getting full. You can say what to keep, for example
  `/compact keep the test failures and the plan`.

Rule of thumb: new task, `/clear`. Same task, getting long, `/compact`.

Run `/clear` now. Then `/context` again: the figure is lower.

## 6. A project `CLAUDE.md`

**Why:** every new conversation starts from nothing. `CLAUDE.md` is a file Claude
Code loads at the start of every session in this folder, so you don't repeat the
same instructions every time. It is advice Claude reads, not a rule it must
obey; Session 3 shows how to enforce things.

1. Generate a first draft:

   ```text
   /init
   ```

   Claude reads the project and writes `CLAUDE.md` in `practice/`. Approve the
   file write. Check it exists:

   ```bash
   ls CLAUDE.md
   ```

2. **Edit it by hand.** `/init` writes what it can discover from the code.
   Your job is to add what it cannot discover, and delete what is vague. Open it
   in your editor (`nano CLAUDE.md` in a terminal) or run `/memory` and pick the
   project file.

   Add these two lines (adjust the wording if you like):

   ```markdown
   - Never edit files in checkpoints/. They are the acceptance tests for this guide.
   - Run tests with `uv run pytest`, and show the summary line before saying a task is done.
   ```

   **Good additions** are specific, checkable, and something Claude would not
   work out by itself:

   - "Never edit files in checkpoints/." Claude can't know they are off limits.
   - "Timestamps are always UTC; `load_csv` converts naive timestamps." Saves a
     wrong guess.

   **Bad additions** are vague or already obvious:

   - "Write clean, high-quality code." Claude can't check it and already tries.
   - "This project uses Python." It can see that.
   - A 50-line copy of the README. It uses up context every session and buries
     the lines that matter. Keep the file short; the docs suggest under 200 lines.

   **Delete any lines that describe what the checkpoint tests expect.** `/init`
   reads `checkpoints/` and may list what Sessions 2 to 5 must build (a `clean`
   module, an outlier filter, how `mean_sample_interval` must behave). Those are
   the answers to later sessions; with them in `CLAUDE.md`, Claude acts on them
   before you get there. Keep only a line saying `checkpoints/` holds the
   acceptance tests and must not be edited.

   Later, to add a line you can also just ask Claude: "Add to CLAUDE.md: ...".
   Read the change before you approve it.

3. Start a new session so the file is loaded: type `/exit`, then run `claude`
   again in `practice/`. Check Claude sees it:

   ```text
   Which files am I not allowed to change in this project?
   ```

   Pass: Claude names `checkpoints/`.

Leave Claude with `/exit` and commit your work (from `practice/`):

```bash
git add src tests CLAUDE.md
git commit -m "feat: summarize; add project CLAUDE.md"
```

From now on `git status` says your branch is ahead of `'origin/main'` and
suggests `git push`. Ignore that: `origin` is the guide repository, which you
can't push to. Session 5 sets up a repository of your own.

## Checkpoint

From `practice/`, in a normal terminal:

```bash
uv run pytest checkpoints/test_session_1.py
uv run pytest
git status checkpoints/
ls CLAUDE.md
```

| Command | Pass |
| :- | :- |
| `uv run pytest checkpoints/test_session_1.py` | Ends with `4 passed` |
| `uv run pytest` | No failures (`6 passed`, or more if Claude added tests) |
| `git status checkpoints/` | Shows no changes (`nothing to commit`) |
| `ls CLAUDE.md` | Prints `CLAUDE.md` |

Stuck? Compare with the reference solution, from the repository root:
`git show reference:practice/src/sensorlog/stats.py`.

## Why it matters

Plan first, so Claude's mistakes are cheap. A misunderstanding caught in a plan
costs one sentence; the same misunderstanding in code costs a review and a redo.
Rewind and `/clear` keep each attempt clean, and `CLAUDE.md` means you write the
important instructions once, not every session.

Next: Session 2, Test-first features (`02-test-first.md`).
