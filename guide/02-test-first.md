# Session 2: Test-first features

About 75 to 90 minutes. By the end `sensorlog` has a `clean` module with three
functions, each built test first: Claude writes a failing test, you watch it
fail, then Claude writes the code until the test passes. You also learn to tell
a test that checks something from one that only looks like it does.

Before you start: Session 1's checkpoint passes, and in `practice/` the command
`uv run pytest checkpoints/test_session_2.py` fails with
`ImportError: cannot import name 'clean' from 'sensorlog'`.

As in Session 1, keep two terminals open: one running Claude, and a second one
where you have run `cd ~/claude-code-starter-guide/practice`, for your own checks.

You don't need to be good at writing tests for this session. You need to be able
to **read** one, which is what the first two sections teach.

## 1. What a test is, in five minutes

**Why:** Claude will write most of your tests. Your job is to judge them. For that
you only need to know their shape.

Open `tests/test_load.py` (from `practice/`: `cat tests/test_load.py`). Each
`test_...` function is one test, and almost every good test has three parts:

```python
def test_load_naive_timestamps_become_utc(tmp_path):
    # Arrange: build the input
    p = tmp_path / "naive.csv"
    p.write_text("timestamp,sensor_id,value\n2026-01-01 00:00:00,temp_1,1.5\n")
    # Act: call the code under test, once
    df = load_csv(p)
    # Assert: compare the result with a value you worked out yourself
    assert df.timestamp[0] == pd.Timestamp("2026-01-01", tz="UTC")
```

(The comments are added here; the file has none.)

- **Arrange**: set up a small input where you know the right answer.
- **Act**: call the function.
- **Assert**: check the result against that answer. `assert x == y` fails the
  test if they differ. `with pytest.raises(ValueError):` passes only if the code
  inside raises that error.

pytest finds every `test_*` function in files named `test_*.py` and runs it.
`uv run pytest` runs the files in `tests/`; `uv run pytest <file>` runs one file.

The question to ask of every test: **if the code were wrong, would this test
fail?** A test that passes whatever the code does is worse than no test, because
it makes you feel safe.

## 2. Spot the useless test

**Why:** Claude sometimes writes tests that pass but check nothing, especially
when you ask it to "make the tests pass". You need to recognise them on sight.

Read `exercises/weak_tests.py`:

```bash
cat exercises/weak_tests.py
```

It holds three tests for `fill_missing`, a function you build later in this
session. You can't run them yet (they import `sensorlog.clean`, which doesn't
exist), and you don't need to: read them. For each, answer the question in its
comment on paper or in your head: what does this test actually check, and which
wrong version of `fill_missing` would still pass?

Then open the answers.

<details>
<summary>Answer key (try first)</summary>

1. **`test_runs`** checks only that `fill_missing` returned something that isn't
   `None`. A version that returns the input unchanged, fills every gap with `0`,
   or returns an empty table all pass. "It runs without error" is not a test of
   behaviour.

2. **`test_matches_itself`** computes the expected value by calling
   `fill_missing`, the function under test, then checks that a second call gives
   the same thing. It compares the code with itself, so any version that gives
   the same answer twice passes, right or wrong. The expected value must come
   from you, not from the code: here, the middle value should be `2.0`.

3. **`test_mocked`** replaces `fill_missing` with a fake (`patch`), calls the
   fake, and checks the fake returned what it was told to return. The real
   function never runs. Any version passes, even one that raises an error. Mocks
   are for replacing things around the code under test (a network call, a
   clock), never the code under test itself.

</details>

You will run these three against your real code at the end of the session.

## 3. Test first: `drop_duplicate_rows`

**Why:** if Claude writes the code first and the tests second, the tests tend to
describe whatever the code happens to do, bugs included. Writing the test first,
and watching it fail, proves the test can fail, so a pass means something.

The pattern has two prompts. **Keep them separate**, and run the tests yourself
between them.

Start Claude in `practice/` (Manual mode). Run `/clear` if you are continuing an
earlier conversation.

**Prompt 1: the failing test.**

```text
Write failing tests for drop_duplicate_rows per this spec; do not implement yet.
Put them in tests/test_clean.py.

Spec, in a new module src/sensorlog/clean.py:
drop_duplicate_rows(df) -> pd.DataFrame
- df has the columns load_csv returns (timestamp, sensor_id, value).
- Removes rows that are exact duplicates of an earlier row; keeps the first.
- Returns a new DataFrame with a fresh index 0..n-1.
- Never modifies the DataFrame passed in.
- An empty DataFrame returns an empty DataFrame with the same columns.
```

Approve the file write. Then run the tests yourself, in your second terminal:

```bash
uv run pytest tests/test_clean.py
```

**Red.** Pass: the run **fails**. Read why. At this stage the right reason is that
the function doesn't exist yet (a `ModuleNotFoundError: No module named
'sensorlog.clean'`, or an `ImportError` or `AttributeError` naming `clean` or
`drop_duplicate_rows`) or isn't implemented. A wrong reason is a typo
or a broken test, for example a `SyntaxError` or a `NameError` inside the test
file: then ask Claude to fix the test, and run it again.

Now freeze the tests. Staging them in git records their current state, so you
can see later whether anything changed them:

```bash
git add tests/test_clean.py
```

(Claude may notice the staged file and mention it, or guess that something else
staged it. That was you; tell it so if it asks.)

**Prompt 2: the code.**

```text
Implement drop_duplicate_rows until tests/test_clean.py passes. Do not modify
the tests. Run uv run pytest tests/test_clean.py and show me the output.
```

Approve the edits. Then check for yourself, in your second terminal:

```bash
uv run pytest tests/test_clean.py
git diff tests/
```

**Green.** Pass: the tests pass, and `git diff tests/` prints **nothing**. (It
shows changes made since you staged the file; nothing means the tests are the
ones you saw fail.) If the diff shows changes, Claude edited the tests to fit the
code. Undo with `/rewind`, and repeat the prompt.

## 4. Repeat for `sort_by_time` and `fill_missing`

Same pattern, one function at a time, with the full prompts below. Run `/clear`
before each function so it starts clean. `src/sensorlog/clean.py` and
`tests/test_clean.py` already exist now; Claude adds to them.

### `sort_by_time`

**Prompt 1:**

```text
Write failing tests for sort_by_time per this spec; do not implement yet.
Add them to tests/test_clean.py, keeping the existing tests.

Spec, in src/sensorlog/clean.py:
sort_by_time(df) -> pd.DataFrame
- df has the columns load_csv returns (timestamp, sensor_id, value).
- Stable sort by (sensor_id, timestamp): rows grouped by sensor_id in ascending
  order, and within each sensor in ascending timestamp order. Rows that tie
  keep their original relative order.
- Returns a new DataFrame with a fresh index 0..n-1.
- Never modifies the DataFrame passed in.
- An empty DataFrame returns an empty DataFrame with the same columns.
```

In your second terminal:

```bash
uv run pytest tests/test_clean.py
```

Red: either an `ImportError` naming `sort_by_time` while collecting
`tests/test_clean.py` (then no test in that file runs, which is expected), or
the new tests fail and the `drop_duplicate_rows` tests pass. Freeze:

```bash
git add tests/test_clean.py
```

**Prompt 2:**

```text
Implement sort_by_time until tests/test_clean.py passes. Do not modify the
tests. Run uv run pytest tests/test_clean.py and show me the output.
```

In your second terminal:

```bash
uv run pytest tests/test_clean.py
git diff tests/
```

Green: all tests pass, and `git diff tests/` prints nothing.

### `fill_missing`

Run `/clear` first.

**Prompt 1:**

```text
Write failing tests for fill_missing per this spec; do not implement yet.
Add them to tests/test_clean.py, keeping the existing tests.

Spec, in src/sensorlog/clean.py:
fill_missing(df, max_gap=pd.Timedelta("5min")) -> pd.DataFrame
- df has the columns load_csv returns (timestamp, sensor_id, value).
- For each sensor separately, fills NaN values by linear interpolation in time
  between the valid samples before and after the gap.
- Only fills when the time between those two surrounding valid samples is at
  most max_gap. Otherwise the value stays NaN.
- Example: one sensor at minutes 0, 1, 2 with values 1, NaN, 3 -> the middle
  becomes 2.0. At minutes 0, 10, 20 with max_gap 5 minutes -> it stays NaN.
- Returns a new DataFrame with a fresh index 0..n-1.
- Never modifies the DataFrame passed in.
- An empty DataFrame returns an empty DataFrame with the same columns.
```

In your second terminal:

```bash
uv run pytest tests/test_clean.py
```

Red: either an `ImportError` naming `fill_missing` while collecting
`tests/test_clean.py` (then no test in that file runs, which is expected), or
the new tests fail and the earlier ones pass. Freeze:

```bash
git add tests/test_clean.py
```

**Prompt 2:**

```text
Implement fill_missing until tests/test_clean.py passes. Do not modify the
tests. Run uv run pytest tests/test_clean.py and show me the output.
```

In your second terminal:

```bash
uv run pytest tests/test_clean.py
git diff tests/
```

Green: all tests pass, and `git diff tests/` prints nothing.

When all three are done, run the checkpoint and commit, in your second terminal:

```bash
uv run pytest checkpoints/test_session_2.py
uv run pytest
git add src tests
git commit -m "feat: clean module, test first"
```

## 5. Would this test fail if the code were wrong?

**Why:** a green run only means something if the tests could have gone red.
Check it the direct way: break the code on purpose and see what notices.

1. **Read the tests Claude wrote.** Open `tests/test_clean.py`. For each test,
   find the Arrange, Act and Assert parts, and check the expected values are
   written out by hand (like `2.0`), not computed by calling the function under
   test. Then ask Claude for a second opinion:

   ```text
   For each test in tests/test_clean.py, name one realistic bug in
   src/sensorlog/clean.py that it would catch. List any test that would not
   catch any bug, and any part of the spec that no test checks.
   ```

   If it finds a gap, have it add a test for it (same two-step pattern).
   Then commit what it added, before you break anything: step 3 puts
   `clean.py` back to its last commit, so uncommitted fixes would be lost.

   ```bash
   git add src tests
   git commit -m "test: close gaps in clean tests"
   ```

   (`nothing to commit` means there was nothing new; carry on.)

2. **Break `fill_missing` on purpose.** Open `src/sensorlog/clean.py` in an
   editor (`nano src/sensorlog/clean.py`). As the **first line of the body** of
   `fill_missing` (right under its `def` line, or under its docstring if it has
   one), add this, indented to match the line below it:

   ```python
       return df.copy().reset_index(drop=True)
   ```

   Now `fill_missing` returns the data without filling anything. Run:

   ```bash
   uv run pytest tests/test_clean.py
   uv run pytest checkpoints/test_session_2.py
   uv run pytest exercises/weak_tests.py
   ```

   Pass: the first two each report **at least one failure**: your tests and the
   checkpoint catch the bug. The third reports `3 passed`: the weak tests
   from section 2 don't notice that `fill_missing` is broken. That is what a
   useless test looks like in practice.

   If `tests/test_clean.py` still passes, your tests don't check filling. Put
   the code back (next step), then ask Claude for a test that would catch it.

3. **Put the code back** and confirm:

   ```bash
   git restore src/sensorlog/clean.py
   uv run pytest
   ```

   Pass: no failures.

## Checkpoint

From `practice/`, in a normal terminal:

```bash
uv run pytest checkpoints/test_session_2.py
uv run pytest
git status checkpoints/
```

| Command | Pass |
| :- | :- |
| `uv run pytest checkpoints/test_session_2.py` | Ends with `7 passed` |
| `uv run pytest` | No failures, and the count includes your tests from `tests/test_clean.py` |
| `git status checkpoints/` | Shows no changes (`nothing to commit`) |

And from section 5: with `fill_missing` broken, `tests/test_clean.py` had at
least one failure.

Stuck? From the repository root:
`git show reference:practice/src/sensorlog/clean.py`. Your version doesn't have
to match; it has to pass.

## Why it matters

A test you have seen fail is a test that can fail. Seeing red first, and checking
with `git diff tests/` that the tests didn't move to meet the code, is what turns
"Claude says the tests pass" into evidence. The habit you practised in section 5,
asking "would this fail if the code were wrong?", is the one that catches the
tests in section 2, which pass whatever the code does.

Next: Session 3, Debugging and automatic checks (`03-debugging-and-checks.md`).
