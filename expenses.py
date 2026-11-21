import math
from datetime import date

TAX_MULTIPLIERS = {
    "food": 1.05,
    "transport": 1.10,
    "entertainment": 1.20,
}

def validate_amount(amount):
    # One exception type (ValueError) for every invalid amount keeps callers simple.
    if isinstance(amount, bool) or not isinstance(amount, (int, float)):
        raise ValueError(f"amount must be a number, got {amount!r}")  # noqa: TRY004
    if not math.isfinite(amount) or amount <= 0:
        raise ValueError(f"amount must be a positive finite number, got {amount!r}")
    return amount


class Expense:
    def __init__(self, amount, category, expense_date=None, description=""):
        self.amount = validate_amount(amount)
        self.category = category
        self.date = expense_date or date.today().isoformat()
        self.description = description

    def to_dict(self):
        return {
            "amount": self.amount,
            "category": self.category,
            "date": self.date,
            "description": self.description,
        }

    @staticmethod
    def from_dict(data):
        return Expense(
            data["amount"], data["category"], data["date"], data["description"]
        )


class ExpenseTracker:
    def __init__(self):
        self.expenses = []

    def add(self, amount, category, expense_date=None, description=""):
        expense = Expense(amount, category, expense_date, description)
        self.expenses.append(expense)
        return expense

    def remove(self, index):
        return self.expenses.pop(index)

    def total(self):
        return sum(e.amount for e in self.expenses)

    def total_by_category(self, category):
        return sum(e.amount for e in self.expenses if e.category == category)

    def final_amount(self, e):
        return e.amount * TAX_MULTIPLIERS.get(e.category, 1.0)

    def total_with_tax(self):
        return sum(self.final_amount(e) for e in self.expenses)

    def format_expense(self, e):
        final = self.final_amount(e)
        return f"{e.date} | {e.category:<14} | {e.amount:>8.2f} | with tax: {final:>8.2f} | {e.description}"