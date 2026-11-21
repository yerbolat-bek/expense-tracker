# AGENTS.md

## Purpose
Console expense tracker (Python). Users add expenses with amount and
category, list them, compute totals (with category tax), and save/load
them as JSON. This is a small educational project.

## Architecture
- `main.py`     : console menu and user input (entry point)
- `expenses.py` : `Expense` and `ExpenseTracker` (business logic, tax rules)
- `storage.py`  : JSON persistence (`save`, `load`)
- `tests/`      : pytest tests
Dependencies flow one way: main -> expenses/storage; storage -> expenses.

## Setup (Windows PowerShell)
    python -m venv venv
    venv\Scripts\Activate.ps1
    pip install -r requirements.txt
Always work inside the venv. Never install packages globally.

## Safe commands (allowed without asking)
    pytest -v
    ruff check .
    mypy --check-untyped-defs expenses.py storage.py main.py
    python -m compileall -q expenses.py storage.py main.py
    git status
    git diff
    git log --oneline

## Commands that need human approval first
- `ruff check --fix` (show the diff before keeping changes)
- `pip install` / upgrading or adding any dependency
- `git commit`, `git checkout`, `git merge`

## Forbidden actions
- No secrets, tokens or real personal/financial data in code, tests or logs.
- No deployments or network calls.
- No destructive commands: `Remove-Item -Recurse`, `git reset --hard`,
  `git clean`, `git push --force`, deleting `.git` or `venv`.
- No unreviewed dependency changes; `requirements.txt` stays pinned.
- Do not move or delete the `baseline` git tag.
- Do not edit or delete tests just to make them pass.
- Do not commit `expenses.json`.

## Coding conventions
- Python 3.13, 4-space indent, sorted imports (ruff rule I001).
- Keep business logic in `expenses.py`; `main.py` only handles I/O.
- Money values must not be silently accepted if invalid (no negative,
  no non-numeric).
- Prefer small, focused changes. One concern per commit.

## Test expectations
- Run `pytest -v` before and after every change; all tests must pass.
- Every bug fix or behavior change needs a test.
- Report exact command output; never claim a test passed without running it.

## Acceptance criteria (must stay true)
1. total() and total_by_category() are correct for valid amounts.
2. Tax: food +5%, transport +10%, entertainment +20%, other 0%.
3. remove(index) with a valid index removes the right expense.
4. save() then load() preserves all expenses.
5. pytest passes in a clean venv with pinned versions.

## Review gates
- A human reviews every diff before it is accepted.
- Agent must summarize: files changed, tests run, results, open risks.

## Known issues (observed, not yet fixed)
- Category is free text and case/whitespace sensitive (tax silently skipped for "Food").
- remove(-1) removes the last item; remove(99) crashes main.py.
- Money uses float.
- load() crashes on corrupt JSON or missing fields.
- main.py does not handle exceptions from save().
- Dev tools (ruff, mypy, pytest-cov) are not pinned; pytest drifts (8.3.3 vs 9.2.0).

## Resolved
- Tax rates deduplicated into TAX_MULTIPLIERS (commit c50e39b).
- Amount validation added (commit 1d5fa0d).
- Atomic JSON save (commit 146e01c).
