import json
from expenses import Expense, ExpenseTracker

DEFAULT_FILE = "expenses.json"


def save(tracker, path=DEFAULT_FILE):
    with open(path, "w") as f:
        json.dump([e.to_dict() for e in tracker.expenses], f)


def load(path=DEFAULT_FILE):
    tracker = ExpenseTracker()
    with open(path) as f:
        data = json.load(f)
    tracker.expenses = [Expense.from_dict(d) for d in data]
    return tracker