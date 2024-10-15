import json
from tabulate import tabulate

# Constants for ANSI escape codes (for colored output)
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
CYAN = '\033[96m'
RESET = '\033[0m'

# Initialize task list
tasks = []

# Load tasks from a file
def load_tasks(filename='tasks.json'):
    """Load tasks from the specified file."""
    global tasks
    try:
        with open(filename, 'r') as file:
            tasks = json.load(file)
    except FileNotFoundError:
        tasks = []
    except json.JSONDecodeError:
        print(RED + "Error loading tasks from file." + RESET)

# Save tasks to a file
def save_tasks(filename='tasks.json'):
    """Save tasks to the specified file."""
    with open(filename, 'w') as file:
        json.dump(tasks, file, indent=4)

# Display tasks in a table format
def show_tasks_table():
    """Display all tasks in a table."""
    if not tasks:
        print(YELLOW + "Your to-do list is empty." + RESET)
    else:
        headers = ["No.", "Task", "Priority", "Status"]
        table_data = [
            [index + 1, task['task'], task['priority'], "✓" if task['done'] else "✗"]
            for index, task in enumerate(tasks)
        ]
        print("\n" + tabulate(table_data, headers, tablefmt="fancy_grid"))

# Get a valid task number from the user
def get_valid_number(prompt, max_value):
    """Prompt the user for a valid task number."""
    while True:
        try:
            task_num = int(input(prompt))
            if 1 <= task_num <= max_value:
                return task_num
            else:
                print(RED + f"Please enter a number between 1 and {max_value}." + RESET)
        except ValueError:
            print(RED + "That's not a valid number, please try again." + RESET)

# Get valid priority input from the user
def get_valid_priority():
    """Prompt the user for a valid task priority."""
    while True:
        priority = input("Set priority (High/Medium/Low): ").capitalize()
        if priority in ['High', 'Medium', 'Low']:
            return priority
        else:
            print(RED + "Please enter a valid priority: High, Medium, or Low." + RESET)

# Add a new task to the list
def add_task():
    """Add a new task with priority."""
    task = input("Enter the task you want to add: ").strip()
    if not task:
        print(RED + "Task cannot be empty!" + RESET)
        return
    priority = get_valid_priority()
    tasks.append({'task': task, 'priority': priority, 'done': False})
    print(GREEN + f"Task '{task}' with priority '{priority}' added." + RESET)

# Delete a task from the list
def delete_task():
    """Delete a task from the list."""
    if not tasks:
        print(YELLOW + "Your to-do list is empty." + RESET)
        return
    show_tasks_table()
    task_num = get_valid_number("Enter the task number to delete: ", len(tasks))
    confirm = input(f"Are you sure you want to delete task {task_num}? (y/n): ").lower()
    if confirm == 'y':
        removed_task = tasks.pop(task_num - 1)
        print(GREEN + f"Task '{removed_task['task']}' deleted." + RESET)
    else:
        print(YELLOW + "Task deletion canceled." + RESET)

# Mark a task as done
def mark_done():
    """Mark a task as completed."""
    if not tasks:
        print(YELLOW + "Your to-do list is empty." + RESET)
        return
    show_tasks_table()
    task_num = get_valid_number("Enter the task number to mark as done: ", len(tasks))
    tasks[task_num - 1]['done'] = True
    print(GREEN + f"Task {task_num} marked as done." + RESET)

# Filter tasks by priority
def filter_tasks(priority):
    """Filter and display tasks based on their priority."""
    filtered_tasks = [task for task in tasks if task['priority'] == priority]
    if filtered_tasks:
        headers = ["No.", "Task", "Priority", "Status"]
        table_data = [
            [index + 1, task['task'], task['priority'], "✓" if task['done'] else "✗"]
            for index, task in enumerate(filtered_tasks)
        ]
        print(f"\n{priority} Priority Tasks:")
        print(tabulate(table_data, headers, tablefmt="fancy_grid"))
    else:
        print(f"No tasks with {priority} priority.")

# Display task summary
def task_summary():
    """Show a summary of the total, completed, and remaining tasks."""
    total = len(tasks)
    done = sum(1 for task in tasks if task.get('done'))
    print(CYAN + f"\nTotal Tasks: {total}, Completed: {done}, Remaining: {total - done}" + RESET)

# Show help menu
def show_help():
    """Display a help menu."""
    print(CYAN + "\nHelp Menu:" + RESET)
    print("1. Show Tasks: Display all your current tasks.")
    print("2. Add Task: Add a new task to your list.")
    print("3. Mark Task as Done: Mark a task as completed.")
    print("4. Delete Task: Remove a task from your list.")
    print("5. Filter by Priority: View tasks based on priority (High/Medium/Low).")
    print("6. Task Summary: View a summary of all tasks.")
    print("7. Help: Show this help menu.")
    print("8. Exit: Save your tasks and exit the application.")

# Main function
def main():
    """Main function to run the task manager."""
    load_tasks()  # Load tasks at the beginning
    while True:
        print("\n" + CYAN + "Menu:" + RESET)
        print("1. Show Tasks")
        print("2. Add Task")
        print("3. Mark Task as Done")
        print("4. Delete Task")
        print("5. Filter by Priority")
        print("6. Task Summary")
        print("7. Help")
        print("8. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            show_tasks_table()
        elif choice == '2':
            add_task()
        elif choice == '3':
            mark_done()
        elif choice == '4':
            delete_task()
        elif choice == '5':
            priority = get_valid_priority()
            filter_tasks(priority)
        elif choice == '6':
            task_summary()
        elif choice == '7':
            show_help()
        elif choice == '8':
            save_tasks()  # Save tasks before exiting
            print(CYAN + "Goodbye!" + RESET)
            break
        else:
            print(RED + "Invalid choice, please try again." + RESET)

# Run the main program
if __name__ == "__main__":
    main()
    