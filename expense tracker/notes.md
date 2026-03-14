## strftime / strptime

`strftime(format)` - converts datetime object to string using format codes

`strptime(string, format)` - opposite of strftime, converts string to datetime object
```python
# strftime example
datetime.now().strftime("%Y-%m-%d")  # "2025-03-14"

# strptime example
datetime.strptime("2025-03-14", "%Y-%m-%d")  # datetime(2025, 3, 14)
```

## Format codes

| Code | Meaning | Example |
|------|---------|---------|
| `%Y` | full year | 2025 |
| `%y` | short year | 25 |
| `%m` | month as number | 03 |
| `%B` | full month name | March |
| `%b` | short month name | Mar |
| `%d` | day of month | 14 |
| `%H` | hour 24h | 17 |
| `%I` | hour 12h | 05 |
| `%M` | minutes | 30 |
| `%S` | seconds | 45 |
| `%p` | AM or PM | PM |
| `%A` | full weekday name | Monday |
| `%a` | short weekday name | Mon |
| `%j` | day of year | 073 |
| `%W` | week number of year | 11 |

---

## f-string column formatting

Used to display data as an aligned table in the terminal.
```python
print(f"{'ID':<5} {'Date':<12} {'Description':<20} {'Amount'}")
print(f"{e['id']:<5} {e['date']:<12} {e['description']:<20} ${e['amount']}")
```

## Alignment symbols
- `<` - align left
- `>` - align right
- `^` - align center

## Width
The number after the symbol sets the minimum column width in characters.
If the value is shorter, it gets padded with spaces.

## Syntax
```python
f"{value:width}"   # right aligned, min width
f"{value:^width}"   # centered, min width
```

## Example
```python
f"{'hi':<10}"   # 'hi        '
f"{'hi':>10}"   # '        hi'
f"{'hi':^10}"   # '    hi    '
```

---

## datetime

`datetime` is a class from the `datetime` module.
```python
from datetime import datetime
```

## Get current date and time
```python
datetime.now()                  # datetime(2025, 3, 14, 17, 30, 45)
datetime.now().year             # 2025
datetime.now().month            # 3
datetime.now().day              # 14
datetime.now().hour             # 17
datetime.now().minute           # 30
datetime.now().second           # 45
```

## Create a specific date
```python
datetime(2025, 3, 14)           # datetime(2025, 3, 14, 0, 0)
datetime(2025, 3, 14, 17, 30)   # datetime(2025, 3, 14, 17, 30)

datetime(2025, 3, 14).year      # 2025
datetime(2025, 3, 14).month     # 3
datetime(2025, 3, 14).day       # 14
```

## Convert string to datetime
```python
datetime.strptime("2025-03-14", "%Y-%m-%d")  # datetime(2025, 3, 14)
```

## Convert datetime to string
```python
datetime(2025, 3, 14).strftime("%Y-%m-%d")   # "2025-03-14"
datetime(2025, 3, 14).strftime("%B %Y")      # "March 2025"
```

---

## argparse

Used to parse command line arguments. Alternative to `sys.argv` but handles
parsing, validation and error handling automatically.
```python
import argparse
```

## Basic setup
```python
# create main parser
parser = argparse.ArgumentParser(prog="app-name")  # prog is shown in --help

# create subparsers to handle subcommands (add, delete, list etc.)
# dest="command" - saves the chosen subcommand into args.command
subparsers = parser.add_subparsers(dest="command")

# register subcommand "add" and save object to variable (needed to add arguments)
add_parser = subparsers.add_parser("add")
add_parser.add_argument("--description", required=True)   # required string
add_parser.add_argument("--amount", type=float, required=True)  # required float

# if subcommand has no arguments - no need to save to variable
subparsers.add_parser("list")

# read what was typed in terminal and store in args
args = parser.parse_args()
```

## Calling functions

`argparse` only parses and stores values - it does NOT call functions itself.
You call functions manually using if/elif:
```python
if args.command == "add":
    add_expense(args.description, args.amount)
elif args.command == "delete":
    delete_expense(args.id)
elif args.command == "list":
    list_expenses()
else:
    parser.print_help()  # show help if no command was given
```

## add_argument options

| Option | Meaning | Example |
|--------|---------|---------|
| `required=True` | argument is mandatory | `--description` must be provided |
| `type=float` | auto converts string to float | `"20"` becomes `20.0` |
| `type=int` | auto converts string to int | `"5"` becomes `5` |

## Accessing values

After `parse_args()` all values are stored in `args`:
```python
args.command      # "add" / "delete" / "list" etc.
args.description  # value of --description
args.amount       # value of --amount (already converted to float)
args.id           # value of --id (already converted to int)
```

## Variable name vs method name

`add_parser` as a variable name is not a conflict with `subparsers.add_parser()` method.
They live in different places:

- `add_parser` - your local variable
- `subparsers.add_parser` - method inside the `subparsers` object

You could name the variable anything - `add_parser` is just a convention for readability.
Real conflict only happens when you overwrite built-in Python names:
```python
list = [1, 2, 3]   # bad - overwrites built-in list()
print = "hello"    # bad - overwrites built-in print()
```