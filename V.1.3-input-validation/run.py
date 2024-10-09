import json
from rich.console import Console
from rich.table import Table

# Initialize the rich console for styled output
console = Console()

# List to store tasks
tasks = []

# Load tasks from JSON file
def load_tasks(filename='tasks.json'):
    global tasks
    try:
        with open(filename, 'r') as file:
            tasks = json.load(file)
    except FileNotFoundError:
        tasks = []
    except json.JSONDecodeError:
        console.print("[red]Error: Could not decode tasks file.[/red]")

# Save tasks to JSON file
def save_tasks(filename='tasks.json'):
    with open(filename, 'w') as file:
        json.dump(tasks, file)

# Display tasks using a rich table
def show_tasks():
    if not tasks:
        console.print("[yellow]Your to-do list is empty.[/yellow]")
    else:
        table = Table(title="To-Do List", show_header=True, header_style="bold cyan")
        table.add_column("No.", justify="right", style="bold magenta", width=3)
        table.add_column("Task", justify="left", style="bold white")
        table.add_column("Priority", justify="center", style="bold blue")
        table.add_column("Status", justify="center", style="bold green")

        for index, task in enumerate(tasks, 1):
            status = "✓" if task.get('done') else "✗"
            table.add_row(str(index), task['task'], task['priority'], status)

        console.print(table)

# Validate the priority input
def validate_priority(priority):
    return priority in ["High", "Medium", "Low"]

# Add a task to the list
def add_task():
    task = console.input("[cyan]Enter the task you want to add: [/cyan]")
    while True:
        priority = console.input("[cyan]Set priority (High/Medium/Low): [/cyan]").capitalize()
        if validate_priority(priority):
            break
        else:
            console.print("[red]Invalid priority! Please enter High, Medium, or Low.[/red]")
    tasks.append({'task': task, 'priority': priority, 'done': False})
    console.print(f"[green]Task '{task}' with priority '{priority}' added to the list.[/green]")

# Delete a task from the list
def delete_task():
    show_tasks()
    if not tasks:
        return  # No tasks to delete

    while True:
        task_num = console.input("[cyan]Enter the task number to delete: [/cyan]")
        if task_num.isdigit() and 1 <= int(task_num) <= len(tasks):
            removed_task = tasks.pop(int(task_num) - 1)
            console.print(f"[green]Task '{removed_task['task']}' deleted.[/green]")
            break
        else:
            console.print("[red]Invalid task number! Please try again.[/red]")

# Mark a task as done
def mark_done():
    show_tasks()
    if not tasks:
        return  # No tasks to mark

    while True:
        task_num = console.input("[cyan]Enter the task number to mark as done: [/cyan]")
        if task_num.isdigit() and 1 <= int(task_num) <= len(tasks):
            tasks[int(task_num) - 1]['done'] = True
            console.print(f"[green]Task {task_num} marked as done![/green]")
            break
        else:
            console.print("[red]Invalid task number! Please try again.[/red]")

# Filter tasks by priority
def filter_tasks():
    while True:
        priority = console.input("[cyan]Enter priority (High/Medium/Low): [/cyan]").capitalize()
        if validate_priority(priority):
            break
        else:
            console.print("[red]Invalid priority! Please enter High, Medium, or Low.[/red]")

    filtered_tasks = [task for task in tasks if task['priority'] == priority]
    if filtered_tasks:
        table = Table(title=f"{priority} Priority Tasks", show_header=True, header_style="bold cyan")
        table.add_column("No.", justify="right", style="bold magenta", width=3)
        table.add_column("Task", justify="left", style="bold white")
        table.add_column("Status", justify="center", style="bold green")

        for index, task in enumerate(filtered_tasks, 1):
            status = "✓" if task.get('done') else "✗"
            table.add_row(str(index), task['task'], status)

        console.print(table)
    else:
        console.print(f"[yellow]No tasks found with {priority} priority.[/yellow]")

# Show task summary
def task_summary():
    total = len(tasks)
    done = sum(1 for task in tasks if task['done'])
    console.print(f"[cyan]Total Tasks: {total}, Completed: {done}, Remaining: {total - done}[/cyan]")

# Show help menu
def show_help():
    console.print("[bold cyan]Help Menu:[/bold cyan]")
    console.print("1. Show Tasks - Display all tasks")
    console.print("2. Add Task - Add a new task")
    console.print("3. Mark Task as Done - Mark a task as completed")
    console.print("4. Delete Task - Delete a task from the list")
    console.print("5. Filter Tasks - View tasks by priority (High/Medium/Low)")
    console.print("6. Task Summary - View summary of tasks")
    console.print("7. Help - Display this help menu")
    console.print("8. Exit - Save and exit the application")

# Main menu loop
def main():
    load_tasks()  # Load tasks when the program starts
    while True:
        console.print("\n[bold cyan]Menu:[/bold cyan]")
        console.print("1. Show Tasks")
        console.print("2. Add Task")
        console.print("3. Mark Task as Done")
        console.print("4. Delete Task")
        console.print("5. Filter by Priority")
        console.print("6. Task Summary")
        console.print("7. Help")
        console.print("8. Exit")

        choice = console.input("[cyan]Enter your choice: [/cyan]")

        if choice == '1':
            show_tasks()
        elif choice == '2':
            add_task()
        elif choice == '3':
            mark_done()
        elif choice == '4':
            delete_task()
        elif choice == '5':
            filter_tasks()
        elif choice == '6':
            task_summary()
        elif choice == '7':
            show_help()
        elif choice == '8':
            save_tasks()  # Save tasks before exiting
            console.print("[cyan]Goodbye![/cyan]")
            break
        else:
            console.print("[red]Invalid choice! Please try again.[/red]")

# Run the program
if __name__ == "__main__":
    main()