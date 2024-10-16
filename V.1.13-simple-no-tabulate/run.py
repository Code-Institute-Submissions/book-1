import json

# ANSI escape codes for colors (alternative to colorama)
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
CYAN = '\033[96m'
RESET = '\033[0m'

tasks = []

# Load tasks from a file
def load_tasks(filename='tasks.json'):
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
    with open(filename, 'w') as file:
        json.dump(tasks, file)

# Display tasks
def show_tasks():
    if not tasks:
        print(YELLOW + "Your to-do list is empty." + RESET)
    else:
        print("\nYour To-Do List:")
        for index, task in enumerate(tasks, 1):
            status = "✓" if task.get('done') else "✗"
            print(f"{index}. {task['task']} [{status}] (Priority: {task['priority']})")

# Get a valid task number
def get_valid_number(prompt, max_value):
    while True:
        try:
            task_num = int(input(prompt))
            if 1 <= task_num <= max_value:
                return task_num
            else:
                print(RED + f"Please enter a number between 1 and {max_value}." + RESET)
        except ValueError:
            print(RED + "That's not a valid number, please try again." + RESET)

# Add a task
def add_task():
    task = input("Enter the task you want to add: ")
    priority = input("Set priority (High/Medium/Low): ").capitalize()
    tasks.append({'task': task, 'priority': priority, 'done': False})
    print(GREEN + f"Task '{task}' with priority '{priority}' added to the list." + RESET)

# Delete a task
def delete_task():
    show_tasks()
    task_num = get_valid_number("Enter the task number to delete: ", len(tasks))
    confirm = input(f"Are you sure you want to delete task {task_num}? (y/n): ").lower()
    if confirm == 'y':
        removed_task = tasks.pop(task_num - 1)
        print(GREEN + f"Task '{removed_task['task']}' deleted." + RESET)
    else:
        print(YELLOW + "Task deletion canceled." + RESET)

# Mark task as done
def mark_done():
    show_tasks()
    task_num = get_valid_number("Enter the task number to mark as done: ", len(tasks))
    tasks[task_num - 1]['done'] = True
    print(GREEN + f"Task {task_num} marked as done." + RESET)

# Filter tasks by priority
def filter_tasks(priority):
    filtered_tasks = [task for task in tasks if task['priority'] == priority]
    if filtered_tasks:
        print(f"\n{priority} Priority Tasks:")
        for index, task in enumerate(filtered_tasks, 1):
            status = "✓" if task.get('done') else "✗"
            print(f"{index}. {task['task']} [{status}]")
    else:
        print(f"No tasks with {priority} priority.")

# Task summary
def task_summary():
    total = len(tasks)
    done = sum(1 for task in tasks if task.get('done'))
    print(CYAN + f"\nTotal Tasks: {total}, Completed: {done}, Remaining: {total - done}" + RESET)

# Help menu
def show_help():
    print(CYAN + "\nHelp Menu:" + RESET)
    print("1. Show Tasks: Display all your current tasks.")
    print("2. Add Task: Add a new task to your list.")
    print("3. Mark Task as Done: Mark a task as completed.")
    print("4. Delete Task: Remove a task from your list.")
    print("5. Filter by Priority: View tasks based on priority (High/Medium/Low).")
    print("6. Exit: Save your tasks and exit the application.")

# Main function
def main():
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
            show_tasks()
        elif choice == '2':
            add_task()
        elif choice == '3':
            mark_done()
        elif choice == '4':
            delete_task()
        elif choice == '5':
            priority = input("Enter priority (High/Medium/Low): ").capitalize()
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