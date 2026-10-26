"""My Budget Tracker - IT215 Final Python Project.

A simple command-line budget manager that stores transactions in a CSV file.
"""

import csv
from datetime import datetime
from pathlib import Path

DATA_FILE = Path(__file__).with_name("budget_transactions.csv")


class BudgetTracker:
    """Keep a list of income and expense transactions."""

    def __init__(self):
        self.transactions = []

    def add_transaction(self, kind, category, amount):
        self.transactions.append({
            "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "type": kind,
            "category": category,
            "amount": amount,
        })

    def totals(self):
        income = sum(t["amount"] for t in self.transactions if t["type"] == "Income")
        expenses = sum(t["amount"] for t in self.transactions if t["type"] == "Expense")
        return income, expenses, income - expenses


def load_transactions(tracker):
    """Load saved transactions when the program starts."""
    if not DATA_FILE.exists():
        return
    try:
        with DATA_FILE.open("r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["type"] not in ("Income", "Expense"):
                    continue
                amount = float(row["amount"])
                if amount < 0:
                    continue
                tracker.transactions.append({
                    "date": row["date"],
                    "type": row["type"],
                    "category": row["category"],
                    "amount": amount,
                })
    except (OSError, ValueError, KeyError, csv.Error) as error:
        print(f"Could not load saved transactions: {error}")


def save_transactions(tracker):
    """Save all transactions to a CSV file."""
    try:
        with DATA_FILE.open("w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=["date", "type", "category", "amount"])
            writer.writeheader()
            writer.writerows(tracker.transactions)
        return True
    except OSError as error:
        print(f"Could not save transactions: {error}")
        return False


def get_amount():
    """Ask for a valid, positive dollar amount."""
    while True:
        try:
            amount = float(input("Enter amount ($): ").strip())
            if not (0 < amount < float("inf")):
                print("Please enter a positive, finite amount.")
                continue
            return round(amount, 2)
        except ValueError:
            print("Please enter a number, such as 25.50.")
        except (EOFError, KeyboardInterrupt):
            print("\nEntry canceled.")
            return None


def add_income(tracker):
    """Record income from work or another source."""
    category = input("Income source (example: Paycheck): ").strip() or "Other Income"
    amount = get_amount()
    if amount is not None:
        tracker.add_transaction("Income", category, amount)
        if save_transactions(tracker):
            print(f"Income of ${amount:.2f} added!")


def add_expense(tracker):
    """Record a purchase or bill."""
    category = input("Expense category (example: Groceries): ").strip() or "Other Expense"
    amount = get_amount()
    if amount is not None:
        tracker.add_transaction("Expense", category, amount)
        if save_transactions(tracker):
            print(f"Expense of ${amount:.2f} added!")


def show_summary(tracker):
    """Show income, expenses, and money remaining."""
    income, expenses, balance = tracker.totals()
    print("\n===== BUDGET SUMMARY =====")
    print(f"Total income:   ${income:.2f}")
    print(f"Total expenses: ${expenses:.2f}")
    print(f"Money remaining: ${balance:.2f}")
    if balance < 0:
        print("Warning: Your expenses are higher than your income.")


def show_history(tracker):
    """List all saved transactions."""
    print("\n===== TRANSACTION HISTORY =====")
    if not tracker.transactions:
        print("No transactions yet.")
        return
    for number, transaction in enumerate(tracker.transactions, start=1):
        print(f"{number}. {transaction['date']} | {transaction['type']} | "
              f"{transaction['category']} | ${transaction['amount']:.2f}")


def main():
    """Display the menu until the user chooses to exit."""
    tracker = BudgetTracker()
    load_transactions(tracker)
    while True:
        print("\n===== MY BUDGET TRACKER =====")
        print("1. Add Income")
        print("2. Add Expense")
        print("3. View Budget Summary")
        print("4. View Transaction History")
        print("5. Exit")
        try:
            choice = input("Choose an option (1-5): ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break
        if choice == "1":
            add_income(tracker)
        elif choice == "2":
            add_expense(tracker)
        elif choice == "3":
            show_summary(tracker)
        elif choice == "4":
            show_history(tracker)
        elif choice == "5":
            print("Goodbye! Your transactions are saved.")
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 5.")


if __name__ == "__main__":
    main()
