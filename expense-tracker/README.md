# Expense Tracker CLI

A command-line tool to manage and track personal expenses, built with Python.

## Requirements

- Python 3.6+
- Terminal

## Setup

This project is part of a larger repository with multiple projects. Clone the whole repo and navigate to this folder:

```bash
git clone https://github.com/eowannx/roadmapsh-python-projects.git
cd expense-tracker
```

## Usage

```bash
python expense_tracker.py <command> [arguments]
```

## Commands

| Command | Description |
|---|---|
| `add --description <text> --amount <number>` | Add a new expense |
| `update --id <id> --description <text> --amount <number>` | Update an expense |
| `delete --id <id>` | Delete an expense |
| `list` | List all expenses |
| `summary` | Show total of all expenses |
| `summary --month <1-12>` | Show total for a specific month |

## Examples

```bash
# Add expenses
python expense_tracker.py add --description "Groceries" --amount 50
# Expense added successfully (ID: 1)

python expense_tracker.py add --description "Netflix" --amount 15

# List all expenses
python expense_tracker.py list
# ID    Date         Description          Amount
# ---------------------------------------------
# 1     2026-03-16   Groceries            $50.0
# 2     2026-03-16   Netflix              $15.0

# Update an expense
python expense_tracker.py update --id 1 --amount 55

# Summary for all time
python expense_tracker.py summary
# Total expenses: $70.0

# Summary for a specific month
python expense_tracker.py summary --month 3
# Total expenses for March: $70.0

# Delete an expense
python expense_tracker.py delete --id 2
```

## How it works

Expenses are saved locally in an `expenses.json` file created automatically on first use. Each expense has:

- `id` — unique identifier
- `date` — date added (YYYY-MM-DD)
- `description` — expense text
- `amount` — expense amount

## Project Source

This project is based on the [Expense Tracker](https://roadmap.sh/projects/expense-tracker) challenge from [roadmap.sh](https://roadmap.sh).