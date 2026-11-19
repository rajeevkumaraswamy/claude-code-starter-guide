# Claude Code Starter Guide

A hands-on guide to the Claude Code CLI that you work through on your own. You build
a small Python project (`sensorlog`, a sensor-log toolkit) with Claude, one session
at a time. Each step is checked against the real state of the project, not against
what Claude says.

Written for Ubuntu 24.04 and an individual Claude Max (5x) plan. Verified against the
official Claude Code docs (https://code.claude.com/docs/en/) in November 2026.

## What you will be able to do afterwards

- Install, update and health-check Claude Code, and know which permission mode,
  model and effort level you are in.
- Run the loop **explore, then plan, then build** instead of "write me X".
- Have Claude write a **failing test first**, then the code, and read the test
  well enough to tell whether it checks anything.
- Reproduce a bug as a failing test before anyone fixes it.
- Accept "done" only with **evidence**: test output you have seen, not a summary.
- Keep a session focused: clear or compact context, rewind when Claude goes off track.
- Use Claude to research docs and the web, and check what it claims.
- Review a diff, commit on a branch and open a pull request.
- Copy the team baseline (`CLAUDE.md`, `.claude/settings.json`, hooks) into a real
  project and adjust it.

## Suggested week

Six sessions of about 1 to 1.5 hours each. Do them in order: each session builds on
the code from the one before.

| Day | Session | You leave with |
| :- | :- | :- |
| 1 | [0. Setup](guide/00-setup.md) | Claude Code installed and logged in, Python toolchain working, a first conversation, permission modes, model and effort, usage |
| 1 or 2 | [1. Working with Claude](guide/01-working-with-claude.md) | Explore, plan, build; plan mode; referencing files; interrupting and rewinding; `/clear` and `/compact`; a project `CLAUDE.md` |
| 2 | [2. Test-first features](guide/02-test-first.md) | Failing test first, then code; reading tests critically; spotting a weak test |
| 3 | [3. Debugging and automatic checks](guide/03-debugging-and-checks.md) | Bug reproduced as a test before the fix; hooks that run ruff and the tests for you |
| 4 | [4. Research](guide/04-research.md) | Reading docs and searching the web with Claude; checking sources; when to use subagents |
| 5 | [5. Review and team baseline](guide/05-review-and-baseline.md) | Reading diffs, branch, pull request, `/code-review`; the shipped team baseline |

Appendices:

- [A. Linux terminal primer](guide/appendix-a-linux-primer.md)
- [B. Cheat sheet](guide/appendix-b-cheat-sheet.md)
- [C. Common problems](guide/appendix-c-troubleshooting.md)

## Prerequisites

- Ubuntu 24.04 with `sudo`, and internet access without a restrictive proxy
  (behind a proxy? see Appendix C).
- An individual **Claude Max** plan. The free claude.ai plan does not include
  Claude Code.
- `git` and `curl`. If either is missing: `sudo apt update && sudo apt install -y git curl`.
- Comfortable with git and Python. You do **not** need to be good at writing tests.
  The guide teaches that part.
- Session 5 uses GitHub and the `gh` CLI. Session 5 tells you how to set them up.

**New to the terminal?** Read [Appendix A](guide/appendix-a-linux-primer.md) first
(about 20 minutes). The rest of the guide assumes you can move between folders, look
at files and stop a running command.

## Get the repository

```bash
cd ~
git clone https://github.com/rajeevkumaraswamy/claude-code-starter-guide.git
cd claude-code-starter-guide
git branch --track reference origin/reference
```

The last line creates a local `reference` branch with the finished solution. You
need it to peek at answers (see "Getting unstuck" below). It does not change your
files.

Layout:

| Folder | What is in it |
| :- | :- |
| `guide/` | The sessions and appendices. Read these. |
| `practice/` | The `sensorlog` project. You start Claude here and do all the exercises here. |
| `practice/checkpoints/` | One test file per session. These tell you whether you finished the session. |
| `baseline/` | The team `CLAUDE.md`, `.claude/settings.json` and hooks. Session 3 copies them into `practice/`; Session 5 explains them. |
| `tools/` | Maintainer tools: the feature ledger and the guide checker. You can ignore them. |
| `site/` | Builds the single-page HTML version of this guide (`site/build_guide.py`). You can ignore it. |

## How checkpoints work

Every session ends with a checkpoint: commands you run and output you compare.
Claude's wording changes from run to run; the checkpoint never depends on it.

Most checkpoints run that session's test file from inside `practice/`:

```bash
cd ~/claude-code-starter-guide/practice
uv run pytest checkpoints/test_session_1.py
```

- Before you do Session N, `checkpoints/test_session_N.py` **fails**. That is
  expected: red now, green after Session N.
- After Session N it passes, and the project's own tests still pass:
  `uv run pytest`.
- **Do not edit the checkpoint files, and do not let Claude edit them.** If Claude
  suggests changing a checkpoint to make it pass, say no. To confirm nobody touched
  them, run `git status checkpoints/`; it should show no changes.

## Getting unstuck

Try these in order:

1. **Read the error.** Run the failing command yourself and read the last 20 lines.
   Paste them to Claude and ask what they mean.
2. **Check the setup.** In your shell, `claude doctor` checks the installation and
   your settings files. Inside a session, `/doctor` runs a fuller checkup and offers
   to fix what it finds.
3. **Look at the reference solution.** The `reference` branch has a finished
   version of the code (`practice/src`). Show one file without changing your
   work, from the repository root:

   ```bash
   git show reference:practice/src/sensorlog/stats.py
   ```

   Swap `stats.py` for the file you want. List them with
   `git ls-tree --name-only reference practice/src/sensorlog/`. Your solution does
   not have to match; it only has to pass the checkpoint.
4. **Appendix C** covers install and login problems, confusing permission prompts,
   usage limits, Claude going off track and long context.
5. **Start the session's exercise again.** From the repository root,
   `git restore practice/` throws away your uncommitted changes to tracked files in
   `practice/` (this cannot be undone). Commit at the end of each session so you
   always have a known-good point to go back to.

## Ground rules this guide follows

- **Built-in Claude Code features only.** No plugins are needed. Session 5 mentions
  some as optional next steps.
- **Evidence before "done".** Every time Claude says it finished, you look at test
  output or a diff before you believe it.
- Claude Code changes often. If a command here does not behave as described, run
  `claude update`, then check the official docs.

## License

MIT. See [LICENSE](LICENSE). Last checked against the Claude Code docs in
November 2026; Claude Code changes often, so verify anything that behaves differently.
