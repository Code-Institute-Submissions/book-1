# ANSI escape codes for colors
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
CYAN = '\033[96m'
RESET = '\033[0m'

# Simple To-Do List in Python with colors using ANSI escape codes

# Initialize an empty list to store tasks
tasks = []

# Function to display tasks
def show_tasks():
    if not tasks:
        print(YELLOW + "Your to-do list is empty." + RESET)
    else:
        print("\nYour To-Do List:")
        for index, task in enumerate(tasks, 1):
            print(f"{index}. {task}")

# Function to add a task
def add_task():
    task = input("Enter the task you want to add: ")
    tasks.append(task)
    print(GREEN + f"Task '{task}' added to the list." + RESET)

# Function to delete a task
def delete_task():
    show_tasks()
    try:
        task_num = int(input("Enter the task number to delete: "))
        if 1 <= task_num <= len(tasks):
            removed_task = tasks.pop(task_num - 1)
            print(GREEN + f"Task '{removed_task}' deleted." + RESET)
        else:
            print(RED + "Invalid task number." + RESET)
    except ValueError:
        print(RED + "Please enter a valid number." + RESET)

# Main function
def main():
    while True:
        print("\n1. Show Tasks")
        print("2. Add Task")
        print("3. Delete Task")
        print("4. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            show_tasks()
        elif choice == '2':
            add_task()
        elif choice == '3':
            delete_task()
        elif choice == '4':
            print(CYAN + "Goodbye!" + RESET)
            break
        else:
            print(RED + "Invalid choice, please try again." + RESET)

if __name__ == "__main__":
    main()