from datetime import date


class Expense:
    def __init__(self, amount, category, expense_date=None, description=""):
        self.amount = amount
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

    def total_with_tax(self):
        total = 0
        for e in self.expenses:
            if e.category == "food":
                total += e.amount * 1.05
            elif e.category == "transport":
                total += e.amount * 1.10
            elif e.category == "entertainment":
                total += e.amount * 1.20
            else:
                total += e.amount
        return total

    def format_expense(self, e):
        if e.category == "food":
            final = e.amount * 1.05
        elif e.category == "transport":
            final = e.amount * 1.10
        elif e.category == "entertainment":
            final = e.amount * 1.20
        else:
            final = e.amount
        return f"{e.date} | {e.category:<14} | {e.amount:>8.2f} | with tax: {final:>8.2f} | {e.description}"