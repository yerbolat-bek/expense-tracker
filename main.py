import os
import storage
from expenses import ExpenseTracker, validate_amount

def main():
    if os.path.exists(storage.DEFAULT_FILE):
        tracker = storage.load()
    else:
        tracker = ExpenseTracker()

    while True:
        print("\n1) Add  2) List  3) Remove  4) Totals  5) Save  0) Exit")
        choice = input("> ")

        if choice == "1":
            try:
                amount = validate_amount(float(input("Amount: ")))
            except ValueError as err:
                print("Invalid amount:", err)
                continue
            category = input("Category (food/transport/entertainment/other): ")
            description = input("Description: ")
            tracker.add(amount, category, description=description)
        elif choice == "2":
            for i, e in enumerate(tracker.expenses):
                print(i, tracker.format_expense(e))
        elif choice == "3":
            index = int(input("Index: "))
            tracker.remove(index)
        elif choice == "4":
            print("Total:", tracker.total())
            print("Total with tax:", tracker.total_with_tax())
        elif choice == "5":
            storage.save(tracker)
            print("Saved.")
        elif choice == "0":
            break


if __name__ == "__main__":
    main()