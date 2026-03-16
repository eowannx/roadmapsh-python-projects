# Task Tracker CLI

A command-line tool to manage tasks, built with Python.

## Requirements

- Python 3.6+
- Terminal

## Setup

This project is part of a larger repository with multiple projects. Clone the whole repo and navigate to this folder:

```bash
git clone https://github.com/eowannx/roadmapsh-python-projects.git
cd task-tracker-cli
```

## Usage

```bash
python task-tracker-cli.py <command> [arguments]
```

## Commands

| Command                         | Description |
|---------------------------------|---|
| `add "task description"`        | Add a new task |
| `update <id> "new description"` | Update task description |
| `delete <id>`                   | Delete a task |
| `mark-in-progress <id>`         | Mark task as in-progress |
| `mark-done <id>`                | Mark task as done |
| `list`                          | List all tasks |
| `list todo`                     | List only todo tasks |
| `list in-progress`              | List only in-progress tasks |
| `list done`                     | List only done tasks |

## Examples

```bash
# Add tasks
python task-tracker-cli.py add "Buy groceries"
# Task added successfully (ID: 1)

python task-tracker-cli.py add "Read a book"
# Task added successfully (ID: 2)

# Update a task
python task-tracker-cli.py update 1 "Buy groceries and cook dinner"

# Mark as in progress
python task-tracker-cli.py mark-in-progress 1

# Mark as done
python task-tracker-cli.py mark-done 2

# List all tasks
python task-tracker-cli.py list
# [1] Buy groceries and cook dinner — in-progress
# [2] Read a book — done

# Delete a task
python task-tracker-cli.py delete 1
```

## How it works

Tasks are saved locally in a `tasks.json` file created automatically on first use. Each task has:

- `id` — unique identifier
- `description` — task text
- `status` — `todo`, `in-progress`, or `done`
- `createdAt` / `updatedAt` — timestamps

## Project Source

This project is based on the [Task Tracker](https://roadmap.sh/projects/task-tracker) challenge from [roadmap.sh](https://roadmap.sh).