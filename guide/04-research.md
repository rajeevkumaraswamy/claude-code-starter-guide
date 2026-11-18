# Session 4: Research

About 75 to 90 minutes. By the end you have used Claude to search the web and
compare ways to find spikes in sensor data; you have checked its sources yourself
and caught a claim they don't support; you have handed a docs lookup to a
subagent; and `sensorlog` has a `flag_outliers` function, built test first.

Before you start: Session 3 is committed, and in `practice/` the command
`uv run pytest checkpoints/test_session_4.py` fails with
`ImportError: cannot import name 'flag_outliers' from 'sensorlog.clean'`.

As before, keep two terminals open: Claude in one, and in the other your own
checks, after `cd ~/claude-code-starter-guide/practice`.

The hooks from Session 3 are on. They matter in section 5, where you
deliberately want a failing test for a while; that section shows how to turn them
off for one step.

## 1. Ask Claude to research

**Why:** Claude can search the web and read pages, which makes it a fast first
pass at "how do people usually do X?". It is also confident whether or not its
sources back it up. This section gets the answer; the next one checks it.

Start Claude in `practice/` (Manual mode) and ask:

```text
How do engineers detect spikes in sensor data robustly? Compare 3 methods,
with sources. Search the web. For each method give: how it works in two or
three sentences, when it fails, and the URL of the page you took it from.
Our data is several sensors sampled about once a minute, with slow drift and
occasional single-sample spikes.
```

**What you will see.** Claude Code asks before Claude uses its two web tools:

- **WebSearch** runs a search and returns titles and links. It doesn't read the
  pages. Claude Code asks before it runs; choose **Yes**.
- **WebFetch** opens one page. In Manual mode it asks before each fetch, except
  for a built-in list of documentation sites it may fetch without asking. The
  prompt shows the address and offers **Yes** (this fetch only), **Yes, and don't
  ask again for** that domain (saves an allow rule in
  `.claude/settings.local.json`, which stays out of git), and **No, and tell
  Claude what to do differently**.

Read each address before you answer. Plain **Yes** is the right default. Use
"don't ask again" only for a documentation site you will come back to.

Expect three methods, or close variants of them: a **z-score** (distance from
the mean in standard deviations), the **IQR rule** (outside the quartiles by
1.5 times their spread), and the **Hampel filter** (distance from a rolling
median, measured in median absolute deviations). Your answer will be worded
differently from anyone else's.

Pass: you have three methods, each with at least one URL.

## 2. Check the sources

**Why:** a link next to a sentence is not evidence that the page says it. Claude
can attach the right link to the wrong claim, or fill a gap with its own
reasoning and cite a page anyway. Even Claude doesn't see the whole page: WebFetch
passes each page through a summarising step and Claude receives the summary. So
the only reliable check is you, reading the page.

1. Ask Claude to tie each claim to its source:

   ```text
   For each claim in your comparison, quote the exact sentence from the source
   that supports it, with the URL. If no source says it and it is your own
   reasoning, write "no source" instead of a quote.
   ```

2. **Open two of the links yourself.** Hold `Ctrl` and click a link in the
   terminal, or copy it into your browser. On each page press `Ctrl+F` and search
   for a few words of the quote.

3. For each claim you checked, decide: the page says it, the page says something
   different, or the page doesn't say it at all.

4. **Find one unsupported claim.** Look for "no source" in Claude's list, a
   quote you couldn't find on the page, or a number (such as a threshold or a
   constant) with no quote behind it. If everything checks out, ask:

   ```text
   Which claims in your comparison are your own reasoning rather than taken
   from a source? Name the one you are least sure of, and why.
   ```

Pass: you opened two sources and found the quoted sentence (or found that it
isn't there), and you can name one claim that no source you checked supports.
Write it down; one line is enough.

This is the habit for research with Claude: **a claim counts once you have seen
it in the source.** Treat the rest as a lead to follow, not an answer.

## 3. Hand a docs lookup to a subagent

**Why:** everything Claude reads stays in the conversation and is sent again on
every turn. A long documentation page you need two sentences from is mostly
noise. A **subagent** is a separate Claude with its own context window: it does
the reading and sends back only a summary. Your main conversation stays short.

You need one detail before you build the Hampel filter: how a centred rolling
window behaves at the start and end of the data. Note the context figure first:

```text
/context
```

Then ask:

```text
Use a subagent to look up in the pandas documentation how Series.rolling
works with center=True and min_periods=1: which samples are in the window
for the first, middle and last rows, for a window of 7. Have it report back
in at most 8 lines, with the URL. Don't paste the page into this
conversation.
```

You see Claude start a subagent (its work shows as a separate task), and you may
be asked to approve the subagent's web fetches; the prompts come to you as
usual. When it finishes, Claude reports a short summary. Run `/context` again:
the figure has grown by far less than a full documentation page would add.

Pass: Claude's answer says that with `center=True` the window is centred on each
row (3 samples either side for a window of 7), and that `min_periods=1` lets the
first and last rows use a shorter window instead of giving NaN.

**When to use a subagent:** a side task that reads a lot and reports a little,
such as a docs lookup, "find every place that calls X", or a survey of a large
folder. **When not to:** anything you want to discuss back and forth, or a small
targeted edit. Each subagent's work also counts toward your plan's usage.

## 4. Choose the method

**Why:** research ends in a decision you can explain. For our data the
Hampel filter is the right one:

| Method | What it compares each value with | Problem for this data |
| :- | :- | :- |
| z-score | The mean and standard deviation of the whole series | One big spike raises the mean and the standard deviation it is measured against, which can hide the spike. Slow drift moves the mean for everything. |
| IQR rule | The quartiles of the whole series | Robust to the spike itself, but global: with drift, the normal values at each end of the series look like outliers, and a spike in the middle can still look normal. |
| Hampel filter | The median and median absolute deviation (MAD) of a small window around it | Robust (a single spike barely moves a median) and local (it follows drift). Two settings: window size and threshold. |

The Hampel filter flags a value when

`|value − median of window| > n_sigmas × 1.4826 × MAD of window`.

The constant 1.4826 scales the MAD so that, for normally distributed noise, it
estimates the standard deviation. `n_sigmas = 3` therefore means roughly "three
standard deviations from local normal".

## 5. Test first: `flag_outliers`

**Why:** the same two-prompt pattern as Session 2. What's new is that the
Stop hook from Session 3 is now running the tests every time Claude finishes.
After Prompt 1 the tests fail on purpose, so the hook would send Claude back to
work, and it would likely implement the function to make them pass. You would
never see red.

So you run **Prompt 1 in a session with hooks off**, and Prompt 2 in a normal
session with the hooks back on.

**Prompt 1, with hooks off.** Leave Claude with `/exit`, then start it again
with hooks turned off for this one session (your files and settings are not
changed):

```bash
claude --settings '{"disableAllHooks": true}'
```

```text
Write failing tests for flag_outliers per this spec; do not implement yet.
Add them to tests/test_clean.py, keeping the existing tests.

Spec, in src/sensorlog/clean.py:
flag_outliers(df, window: int = 7, n_sigmas: float = 3.0) -> pd.Series
- A Hampel filter. df has the columns load_csv returns (timestamp,
  sensor_id, value), possibly not sorted.
- Returns a bool Series aligned to df.index (same index labels as df).
- Computed for each sensor_id separately, in timestamp order.
- For each value, take a centred rolling window of `window` samples of the
  same sensor, with min_periods=1 (shorter windows at the ends). Using the
  non-NaN values in the window, compute the median and the MAD (median of
  absolute deviations from that median).
- Flag the value when |value - median| > n_sigmas * 1.4826 * MAD
  (strictly greater).
- NaN values are never flagged. A sensor whose values are all NaN gives all
  False.
- Example: one sensor, 11 samples one minute apart, all 10.0 except 100.0 at
  position 5 -> only position 5 is True. The same rows shuffled -> the same
  flags, by index label.
- Never modifies the DataFrame passed in.
```

Run the tests yourself, in your second terminal:

```bash
uv run pytest tests/test_clean.py
```

**Red.** Pass: the new tests fail because `flag_outliers` doesn't exist (an
`ImportError` naming `flag_outliers`) or isn't implemented; the tests from
Session 2 still pass. If the failure is a typo or a broken test, ask Claude to
fix the test, and run it again.

Leave this session with `/exit`, then freeze the tests:

```bash
git add tests/test_clean.py
```

**Prompt 2, hooks back on.** Start Claude normally:

```bash
claude
```

```text
Implement flag_outliers in src/sensorlog/clean.py until tests/test_clean.py
passes. Do not modify the tests. Run uv run pytest tests/test_clean.py and
show me the output.
```

Approve the edits. When Claude finishes, the Stop hook runs the whole test suite;
if anything is still red, you see Claude carry on with a message from the hook.
Then check for yourself, in your second terminal:

```bash
uv run pytest tests/test_clean.py
git diff tests/
uv run pytest checkpoints/test_session_4.py
```

**Green.** Pass: the tests pass; `git diff tests/` prints **nothing**; the
checkpoint ends with `5 passed`. If the checkpoint fails while your own tests
pass, your tests missed part of the spec: paste the checkpoint failure to Claude
and ask which part of the spec your tests don't check, then add a test for it
(same two-step pattern).

**One question to ask of the result.** Ask Claude:

```text
What does flag_outliers do on a stretch where every value is identical
except one that differs by 0.001? Explain using the formula, then say
whether that is what we want for real sensor data.
```

(Answer: the MAD of a perfectly flat window is 0, so any value that differs at
all is flagged. Real sensors are rarely perfectly flat, but quantised or stuck
sensors are. It is a known limit of the method, worth a comment in the code, not a
bug in your function.)

Leave Claude with `/exit` and commit:

```bash
git add src tests
git commit -m "feat: flag_outliers (Hampel filter), test first"
```

## Checkpoint

From `practice/`, in a normal terminal:

```bash
uv run pytest checkpoints/test_session_4.py
uv run pytest
git status checkpoints/
```

| Command | Pass |
| :- | :- |
| `uv run pytest checkpoints/test_session_4.py` | Ends with `5 passed` |
| `uv run pytest` | No failures, and includes your new `flag_outliers` tests |
| `git status checkpoints/` | Shows no changes (`nothing to commit`) |

And from section 2: you opened two sources yourself and wrote down one claim
they don't support.

Stuck? From the repository root:
`git show reference:practice/src/sensorlog/clean.py`.

## Why it matters

Claude makes research fast, but a summary with links is a set of leads, not a
set of facts, until you have seen the sentence on the page. Subagents let you
send it off to read a lot without filling your conversation. And the hooks keep
working for you once the session is test-first: you switch them off only for the
one step where red is the goal.

Next: Session 5, Review and team baseline (`05-review-and-baseline.md`).
