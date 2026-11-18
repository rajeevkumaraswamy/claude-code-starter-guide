# Session 3: Debugging and automatic checks

About 75 to 90 minutes. By the end you have fixed a real bug in `sensorlog` the
disciplined way (reproduce it as a failing test, find the cause, fix the code,
never the test), and the project has two hooks: one runs ruff after every edit
Claude makes, the other runs the tests before Claude may say it is finished.

Before you start: Sessions 1 and 2 are committed, and `uv run pytest` passes in
`practice/`.

## 1. A failing check

**Why:** this time you don't know what's wrong. Bugs arrive as a failing check or
a wrong number, and the temptation (yours and Claude's) is to change things until
the check goes green. This section is about not doing that.

From `practice/`, run the Session 3 checkpoint **on its own**:

```bash
uv run pytest checkpoints/test_session_3.py
```

Pass (for now): it **fails** with `1 failed, 1 passed`, and the failure is an
`AssertionError` for `test_out_of_order_rows`, containing
`assert 30.0 == 60.0`.

(Run this file on its own. If you run it together with the Session 4 or 5
checkpoints, pytest stops early with an `ImportError` from those files, for code
you haven't built yet, and you never see this failure.)

Read the test to see what it expects:

```bash
cat checkpoints/test_session_3.py
```

So `mean_sample_interval` returns 30 seconds where 60 is expected. You don't yet
know why, and neither does Claude. Keep it that way until you have evidence.

## 2. Reproduce, then find the cause, then fix

**Why:** a bug you have reproduced as a test in `tests/` can't quietly come back:
the project's own test suite now guards it. Finding the cause before changing
code stops Claude from "fixing" a symptom, or the test.

**The rule for this whole guide: never ask Claude to "fix the test" or "make the
tests pass".** Those words invite it to change the test until it agrees with the
broken code. Say instead:

> Fix the code so this test passes. Do not modify the tests.

Start Claude in `practice/` (Manual mode). Raise effort for this debugging
stretch with `/effort high` (Session 0, section 6).

**Step 1: reproduce.**

```text
uv run pytest checkpoints/test_session_3.py fails. Reproduce this as a failing
test in tests/ first, in tests/test_stats.py, using a small DataFrame where
the expected answer is easy to work out by hand. Do not change anything in
src/ yet. Run the new test and show me the pytest output.
```

Approve the test edit and the test run. **Evidence, not summaries:** if Claude
answers "the test fails as expected" without the output, ask for it:

```text
Show me the pytest output.
```

Then run it yourself (second terminal):

```bash
uv run pytest tests/test_stats.py
```

Pass: exactly one test fails, the new one, with an `AssertionError` (not an
`ImportError` or a typo). Freeze it:

```bash
git add tests/test_stats.py
```

**Step 2: find the root cause.**

```text
Now find the root cause in src/sensorlog/stats.py. Explain it, and show me
evidence: the intermediate values for the failing input. Don't change any
file yet.
```

Read the explanation. Does the evidence match the numbers in the failure? If
the explanation doesn't account for exactly `30.0` instead of `60.0`, push back.

**Step 3: fix.**

```text
Fix the code so this test passes. Do not modify the tests. Then run
uv run pytest checkpoints/test_session_3.py and uv run pytest, and show me
both outputs.
```

Then check for yourself:

```bash
uv run pytest checkpoints/test_session_3.py
uv run pytest
git diff tests/
git status checkpoints/
```

Pass: the checkpoint ends with `2 passed`; `uv run pytest` has no failures;
`git diff tests/` prints **nothing** (the reproduction test is the one you saw
fail); `git status checkpoints/` shows no changes.

<details>
<summary>What the bug was (read after you've fixed it)</summary>

`mean_sample_interval` took the timestamps for one sensor in file order and
averaged the differences between neighbours. With rows at 0, 120 and 60 seconds,
the differences are +120 and −60, which average to 30. Sorted (0, 60, 120), they
are 60 and 60. Real logs do have out-of-order rows: `data/messy.csv` has several.
The fix is to sort the timestamps before taking differences.

</details>

Set effort back with `/effort auto`, leave Claude with `/exit`, and commit:

```bash
git add src tests
git commit -m "fix: mean_sample_interval ignores file order"
```

## 3. Hooks: checks Claude can't forget

**Why:** `CLAUDE.md` is advice. Claude usually follows it, but nothing makes it.
A **hook** is a shell command that Claude Code itself runs at a fixed moment, such
as after every file edit, or when Claude tries to finish. Claude can't skip it.
The repository ships two in `baseline/.claude/`:

| Hook | When it runs | What it does |
| :- | :- | :- |
| `lint-after-edit.sh` | After Claude edits or writes a file (`PostToolUse`, tools `Edit` and `Write`) | For `.py` files: `ruff check --fix`, then `ruff format`. Problems ruff can't fix go back to Claude. |
| `tests-before-stop.sh` | When Claude tries to finish its turn (`Stop`) | Runs `uv run pytest -q` (the tests in `tests/`). If they fail, Claude is told to keep working. |

The same folder's `settings.json` also lets Claude run `uv run pytest` and
`uv run ruff` without asking, so you'll see fewer prompts from now on.

**Install them.** You installed hooks only now, after the fix, on purpose: in
step 1 you wanted a failing test, and the Stop hook would have pushed Claude to
fix it straight away. Copy only the `.claude` folder (you keep your own
`CLAUDE.md` from Session 1; Session 5 looks at the team one). From the repository
root:

```bash
cd ~/claude-code-starter-guide
cp -R baseline/.claude practice/
ls practice/.claude practice/.claude/hooks
```

Pass: you see `hooks` and `settings.json`, then `lint-after-edit.sh` and
`tests-before-stop.sh`. (If `.claude` in `practice/` already held a
`settings.local.json` from earlier "don't ask again" answers, it is still there;
that is fine.)

Start a new session so the new settings are loaded for certain:

```bash
cd ~/claude-code-starter-guide/practice
claude
```

If Claude Code asks whether you trust this folder, accept: hooks don't run in a
folder you haven't trusted. Then:

```text
/hooks
```

Pass: the list shows a `PostToolUse` hook and a `Stop` hook. Press `Esc` to close
it.

### Watch the lint hook fix an edit

Ask Claude to write a deliberately messy file:

```text
This is a test of the lint hook. Create src/sensorlog/scratch.py with exactly
this content, unused imports and spacing included, and do nothing else:

import os
import sys
def double(x):
    return x*2
```

Approve the write. The hook runs right after it. Then look at the file (second
terminal, from `practice/`):

```bash
cat src/sensorlog/scratch.py
uv run ruff check .
```

Pass: the file is now only

```python
def double(x):
    return x * 2
```

(the unused imports are gone and `x*2` became `x * 2`), and `ruff check` prints
`All checks passed!`. Claude wrote the messy version; the hook cleaned it.

If the file still has the imports, check that `/hooks` lists the hooks and that
you started a new session after copying them. If Claude "tidied" the content
before writing, ask it again to write it exactly as given.

Remove the scratch file:

```bash
rm src/sensorlog/scratch.py
```

### Watch the Stop hook push back

Now give Claude a test that is wrong on purpose:

```text
This is a test of the Stop hook. Add this test to the end of
tests/test_stats.py, exactly as written, and then stop. Do not run the tests.

def test_stop_hook_demo():
    assert mean_sample_interval(_df([0, 60, 180]), "temp_1") == 60.0
```

The real answer is 90 seconds, so the test fails. When Claude tries to finish,
the Stop hook runs the tests, sees the failure, and sends Claude back to work
with the last lines of the pytest output and the instruction not to weaken the
test. You see Claude continue after it had stopped, with a message from the Stop
hook. It should then say the test's expected value looks wrong and ask you,
rather than change the code to match it.

Undo it with `/rewind`: pick the "This is a test of the Stop hook" prompt and
choose **Restore code and conversation**. Then check (second terminal):

```bash
git diff tests/
```

Pass: prints nothing.

**Exit code 2, in one paragraph.** A hook tells Claude Code what happened through
its exit code. `0` means all is well; carry on. `2` means "Claude, look at this":
whatever the script printed to stderr is handed to Claude. After an edit
(`PostToolUse`) the edit has already happened, so Claude just reads the message
and fixes the problem; at `Stop`, exit 2 also stops Claude from finishing. Any
other code means the hook itself broke: you see a warning, and Claude carries on
as if there were no hook. The Stop hook pushes back only once per turn: if Claude
tries to stop again while tests still fail, the hook lets it, so it can't loop
forever.

Later, when you deliberately want a failing test for a while (test-first work),
start that session with hooks off: `claude --settings '{"disableAllHooks": true}'`.

Leave Claude with `/exit` and commit the hooks:

```bash
git add .claude/settings.json .claude/hooks
git commit -m "chore: add team hooks"
```

## Checkpoint

From `practice/`, in a normal terminal:

```bash
uv run pytest checkpoints/test_session_3.py
uv run pytest
git status checkpoints/
ls .claude/hooks
```

| Command | Pass |
| :- | :- |
| `uv run pytest checkpoints/test_session_3.py` | Ends with `2 passed` |
| `uv run pytest` | No failures, and includes your reproduction test |
| `git status checkpoints/` | Shows no changes (`nothing to commit`) |
| `ls .claude/hooks` | Lists `lint-after-edit.sh` and `tests-before-stop.sh` |

And from section 3: after Claude wrote `scratch.py`, `cat` showed it reformatted
to `return x * 2` with no imports, and `uv run ruff check .` printed
`All checks passed!`.

Stuck? From the repository root:
`git show reference:practice/src/sensorlog/stats.py`.

## Why it matters

The failing test came first, so you know it catches this bug, and it stays in
`tests/`, so the bug can't return unnoticed. The cause came before the fix, so
the fix is to the code, not to the check. And the hooks move two habits, lint
your edits and run the tests before saying "done", out of Claude's good
intentions and into something that runs every time.

Next: Session 4, Research (`04-research.md`).
