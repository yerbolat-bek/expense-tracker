import json
import os
import tempfile

from expenses import Expense, ExpenseTracker

DEFAULT_FILE = "expenses.json"


def save(tracker, path=DEFAULT_FILE):
    data = [e.to_dict() for e in tracker.expenses]
    directory = os.path.dirname(os.path.abspath(path))
    fd, tmp_path = tempfile.mkstemp(dir=directory, suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(data, f)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp_path, path)
    except BaseException:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
        raise


def load(path=DEFAULT_FILE):
    tracker = ExpenseTracker()
    with open(path) as f:
        data = json.load(f)
    tracker.expenses = [Expense.from_dict(d) for d in data]
    return tracker