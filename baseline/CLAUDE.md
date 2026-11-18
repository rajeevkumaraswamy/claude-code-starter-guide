# Project instructions for Claude

## Commands

- Test: `uv run pytest -q`
- Lint: `uv run ruff check .` (auto-fix: `uv run ruff check --fix .`)
- Format: `uv run ruff format .`
- Run one test: `uv run pytest -q tests/test_file.py::test_name`

Hooks in `.claude/settings.json` already run ruff after every edit to a `.py`
file and run the tests when you try to finish. Treat their messages as real
failures to fix, not noise.

## How to work here

- Write or update a failing test before changing behavior. Run it and show
  that it fails, then change the code.
- Show test output before claiming done. "Should work" is not done; paste the
  `uv run pytest -q` summary line.
- Never weaken or delete a test to make it pass; ask first. If a test looks
  wrong, say why and wait.
- No new dependencies without asking. That includes `uv add` and new imports
  of packages that are not already in `pyproject.toml`.
- Keep changes small and focused on the request. Mention anything else you
  notice instead of fixing it unasked.
- Do not read `.env` files or anything under `secrets/`.

## This project

<!-- Fill in each placeholder below, delete this comment, and commit. -->

- What it does: <ONE SENTENCE ABOUT THE PROJECT>
- Code lives in: <e.g. src/your_package/>
- Tests live in: <e.g. tests/>
- Python version: <e.g. 3.12>
- Data or fixtures: <WHERE TEST DATA LIVES, OR "none">
- Never touch: <GENERATED FILES, VENDORED CODE, MIGRATIONS ...>
- Conventions: <NAMING, TYPE HINTS, DOCSTRING STYLE ...>
- Ask before: <ANYTHING RISKY HERE, e.g. changing the public API>
