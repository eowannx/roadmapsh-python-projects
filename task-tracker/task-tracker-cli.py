import sys
import json
import os
from datetime import datetime

# File where we will save our tasks
TASKS_FILE = "tasks.json"


def load_tasks():
    # This function loads tasks from JSON file. If there is no JSON file, it returns empty list
    # Called at the start of most commands to get up-to-date data
    if not os.path.exists(TASKS_FILE):
        return []
    with open(TASKS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)
    # encoding=“utf-8” — the encoding needed to correctly display non-English characters.
    # However, without specifying the encoding, Python uses the system's default encoding,
    # which on Windows is often not UTF-8 but cp1252 or another encoding.
    # The code may work for me, but it will break for someone using a different system.
    # Therefore, the standard practice is to always explicitly specify encoding="utf-8", unless the text is purely English.

def save_tasks(tasks):
    # This function saves list of tasks into JSON file
    # Called at the end of write commands to persist changes
    with open(TASKS_FILE, "w", encoding="utf-8") as f:
        json.dump(tasks, f, indent=2, ensure_ascii=False)
    # indent=2 for readable formatting
    # ensure_ascii=False: by default, the json.dump() function converts non-English characters into Unicode sequences
    # for example, “привет” → “\u043f\u0440\u0438\u0432\u0435\u0442”
    # disabling it writes characters as-is, which works because the file is opened with encoding="utf-8"


def get_next_id(tasks):
    # This function generates next ID - adding 1 to max existing one
    if not tasks:
        return 1
    return max(task["id"] for task in tasks) + 1


def add_task(description):
    tasks = load_tasks()
    now = datetime.now().isoformat()
    # datetime.now() returns the current time in the format “2026-03-15T10:30:00”
    # .isoformat() converts the datetime object to a string

    new_task = {
        "id": get_next_id(tasks),
        "description": description,
        "status": "todo",  # By default new task in status "todo"
        "createdAt": now,
        "updatedAt": now,
    }

    tasks.append(new_task)
    save_tasks(tasks)
    print(f"Task added successfully (ID: {new_task['id']})")


def update_task(task_id, new_description):
    tasks = load_tasks()

    # Looking for task by ID in list
    for task in tasks:
        if task["id"] == task_id:
            task["description"] = new_description
            task["updatedAt"] = datetime.now().isoformat()
            save_tasks(tasks)
            print(f"Task {task_id} updated successfully")
            return

    print(f"Error: Task with ID {task_id} not found")


def delete_task(task_id):
    tasks = load_tasks()

    # Save all tasks except the one we need to delete (list comprehension)
    filtered = [task for task in tasks if task["id"] != task_id]

    # If the length hasn't changed, it means that no task has been deleted;
    # in other words, there is no task with that ID.
    if len(filtered) == len(tasks):
        print(f"Error: Task with ID {task_id} not found")
        return

    save_tasks(filtered)
    print(f"Task {task_id} deleted successfully")


def mark_task(task_id, status):
    # This function change status of the task
    tasks = load_tasks()

    for task in tasks:
        if task["id"] == task_id:
            task["status"] = status
            task["updatedAt"] = datetime.now().isoformat()
            save_tasks(tasks)
            print(f"Task {task_id} marked as {status}")
            return

    print(f"Error: Task with ID {task_id} not found")


def list_tasks(status_filter=None):
    # return list of tasks in terminal
    # status_filter - if given, shows only tasks with that status
    tasks = load_tasks()

    if status_filter:
        tasks = [task for task in tasks if task["status"] == status_filter]

    if not tasks:
        print("No tasks found")
        return

    for task in tasks:
        print(f"[{task['id']}] {task['description']} — {task['status']}")


def print_help():
    print("""
Usage:
  python task-tracker-cli.py add "Task description"
  python task-tracker-cli.py update <id> "New description"
  python task-tracker-cli.py delete <id>
  python task-tracker-cli.py mark-in-progress <id>
  python task-tracker-cli.py mark-done <id>
  python task-tracker-cli.py list
  python task-tracker-cli.py list done
  python task-tracker-cli.py list todo
  python task-tracker-cli.py list in-progress
""")


def main():
    # sys.argv — list of command line arguments
    # sys.argv[0] — name of the script file
    # sys.argv[1] — first argument (command) and etc
    args = sys.argv[1:]  # takes everything except the script name

    if not args:
        print_help()
        return

    command = args[0]

    if command == "add":
        if len(args) < 2:
            print("Error: Please provide a task description")
            return
        add_task(args[1])

    elif command == "update":
        if len(args) < 3:
            print("Error: Please provide task ID and new description")
            return
        update_task(int(args[1]), args[2])  # int() converts string "1" to number 1

    elif command == "delete":
        if len(args) < 2:
            print("Error: Please provide task ID")
            return
        delete_task(int(args[1]))

    elif command == "mark-in-progress":
        if len(args) < 2:
            print("Error: Please provide task ID")
            return
        mark_task(int(args[1]), "in-progress")

    elif command == "mark-done":
        if len(args) < 2:
            print("Error: Please provide task ID")
            return
        mark_task(int(args[1]), "done")

    elif command == "list":
        if len(args) == 1:
            list_tasks()  # Without filter - all tasks
        else:
            status = args[1]
            if status not in ("done", "todo", "in-progress"):
                print("Error: Status must be 'done', 'todo', or 'in-progress'")
                return
            list_tasks(status)

    else:
        print(f"Error: Unknown command '{command}'")
        print_help()


# This block executes only if file executed directly
# (and not imported as a module in another file)
if __name__ == "__main__":
    main()