import argparse
import json
import os
from datetime import datetime

# File where we will save expenses
DATA_FILE = "expenses.json"

# This function loads tasks from JSON file. If there is no JSON file, it returns empty list
# Called at the start of most commands to get up-to-date data
def load_expenses():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

# This function saves list of tasks into JSON file
# Called at the end of write commands to persist changes
def save_expenses(expenses):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(expenses, f, indent=2, ensure_ascii=False)

# IDs only grow, deleted IDs are never reused (intentional)
def get_next_id(expenses):
    if not expenses:
        return 1
    return max(e["id"] for e in expenses) + 1

def add_expense(description, amount):
    if amount <= 0:
        print("Error: Amount must be a positive number.")
        return

    expenses = load_expenses()
    expense = {
        "id": get_next_id(expenses),
        "date": datetime.now().strftime("%Y-%m-%d"), # see notes.md: strftime / strptime
        "description": description,
        "amount": amount,
    }
    expenses.append(expense)
    save_expenses(expenses)
    print(f"Expense added successfully (ID: {expense['id']})")


def update_expense(expense_id, description, amount):
    expenses = load_expenses()

    for expense in expenses:
        if expense["id"] == expense_id:
            if description:
                expense["description"] = description
            if amount is not None:
                if amount <= 0:
                    print("Error: Amount must be a positive number.")
                    return
                expense["amount"] = amount
            save_expenses(expenses)
            print(f"Expense updated successfully (ID: {expense_id})")
            return

    print(f"Error: Expense with ID {expense_id} not found.")


def delete_expense(expense_id):
    expenses = load_expenses()
    # Save all tasks except the one we need to delete (list comprehension)
    new_expenses = [e for e in expenses if e["id"] != expense_id]

    # If the length hasn't changed, it means that no task has been deleted;
    if len(new_expenses) == len(expenses):
        print(f"Error: Expense with ID {expense_id} not found.")
        return

    save_expenses(new_expenses)
    print(f"Expense deleted successfully")


def list_expenses():
    expenses = load_expenses()

    if not expenses:
        print("No expenses found.")
        return

    # table header, columns aligned by min width (see notes: f-string column formatting)
    print(f"{'ID':<5} {'Date':<12} {'Description':<20} {'Amount'}")
    print("-" * 45) # separator line, "-" repeated 45 times
    for e in expenses:
        print(f"{e['id']:<5} {e['date']:<12} {e['description']:<20} ${e['amount']}")


def summary(month=None):
    expenses = load_expenses()

    if month:
        current_year = datetime.now().year # see notes: datetime
        filtered = [
            e for e in expenses
            if datetime.strptime(e["date"], "%Y-%m-%d").month == month
               and datetime.strptime(e["date"], "%Y-%m-%d").year == current_year
        ]
        total = sum(e["amount"] for e in filtered)
        month_name = datetime(current_year, month, 1).strftime("%B")
        print(f"Total expenses for {month_name}: ${total}")
    else:
        total = sum(e["amount"] for e in expenses)
        print(f"Total expenses: ${total}")


def main():
    parser = argparse.ArgumentParser(prog="expense-tracker") # prog is shown in --help
    subparsers = parser.add_subparsers(dest="command") # dest saves chosen subcommand into args.command

    # add - save to variable to attach arguments
    add_parser = subparsers.add_parser("add")
    add_parser.add_argument("--description", required=True)
    add_parser.add_argument("--amount", type=float, required=True) # type=float auto converts string to float

    # update - save to variable to attach arguments
    update_parser = subparsers.add_parser("update")
    update_parser.add_argument("--id", type=int, required=True) # type=int auto converts string to int
    update_parser.add_argument("--description")
    update_parser.add_argument("--amount", type=float)

    # delete - save to variable to attach arguments
    delete_parser = subparsers.add_parser("delete")
    delete_parser.add_argument("--id", type=int, required=True)

    # list - no arguments, no need to save to variable
    subparsers.add_parser("list")

    # summary - save to variable to attach arguments
    summary_parser = subparsers.add_parser("summary")
    summary_parser.add_argument("--month", type=int)

    # reads terminal input and stores all values in args
    args = parser.parse_args()

    # argparse parses, we call functions manually (see notes: argparse)
    if args.command == "add":
        add_expense(args.description, args.amount)
    elif args.command == "update":
        update_expense(args.id, args.description, args.amount)
    elif args.command == "delete":
        delete_expense(args.id)
    elif args.command == "list":
        list_expenses()
    elif args.command == "summary":
        summary(args.month)
    else:
        parser.print_help()

# This block executes only if file executed directly
# (and not imported as a module in another file)
if __name__ == "__main__":
    main()