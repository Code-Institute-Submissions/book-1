import json
from rich.console import Console
from rich.table import Table
from datetime import datetime

# Ascii art
ascii_art = r'''
 /$$$$$$$$                /$$$$$$$                  /$$       /$$             /$$    
|__  $$__/               | $$__  $$                | $$      |__/            | $$    
   | $$  /$$$$$$         | $$  \ $$  /$$$$$$       | $$       /$$  /$$$$$$$ /$$$$$$  
   | $$ /$$__  $$ /$$$$$$| $$  | $$ /$$__  $$      | $$      | $$ /$$_____/|_  $$_/  
   | $$| $$  \ $$|______/| $$  | $$| $$  \ $$      | $$      | $$|  $$$$$$   | $$    
   | $$| $$  | $$        | $$  | $$| $$  | $$      | $$      | $$ \____  $$  | $$ /$$
   | $$|  $$$$$$/        | $$$$$$$/|  $$$$$$/      | $$$$$$$$| $$ /$$$$$$$/  |  $$$$/
   |__/ \______/         |_______/  \______/       |________/|__/|_______/    \___/  
'''

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
        table.add_column("Due Date", justify="center", style="bold yellow")
        table.add_column("Status", justify="center", style="bold green")

        for index, task in enumerate(tasks, 1):
            status = "✅" if task.get('done') else "❌"  # Use emoticons here
            due_date = task.get('due_date', 'N/A')
            table.add_row(str(index), task['task'], task['priority'], due_date, status)

        console.print(table)

# Validate the priority input
def validate_priority(priority):
    return priority in ["High", "Medium", "Low"]

# Validate the date input
def validate_date(date_text):
    try:
        datetime.strptime(date_text, '%Y-%m-%d')
        return True
    except ValueError:
        return False

# Add a task to the list
def add_task():
    task = console.input("[cyan]Enter the task you want to add: [/cyan]")
    while True:
        priority = console.input("[cyan]Set priority (High/Medium/Low): [/cyan]").capitalize()
        if validate_priority(priority):
            break
        else:
            console.print("[red]Invalid priority! Please enter High, Medium, or Low.[/red]")

    # Get due date
    while True:
        due_date = console.input("[cyan]Enter due date (YYYY-MM-DD): [/cyan]")
        if validate_date(due_date):
            break
        else:
            console.print("[red]Invalid date format! Please use YYYY-MM-DD.[/red]")

    tasks.append({'task': task, 'priority': priority, 'due_date': due_date, 'done': False})
    console.print(f"[green]Task '{task}' with priority '{priority}' and due date '{due_date}' added to the list.[/green]")

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

# Edit an existing task
def edit_task():
    show_tasks()
    if not tasks:
        return  # No tasks to edit

    while True:
        task_num = console.input("[cyan]Enter the task number to edit: [/cyan]")
        if task_num.isdigit() and 1 <= int(task_num) <= len(tasks):
            task_index = int(task_num) - 1
            task = tasks[task_index]
            
            console.print(f"[yellow]Editing Task: {task['task']} (Priority: {task['priority']}, Due Date: {task['due_date']})[/yellow]")
            new_task = console.input("[cyan]Enter the new task description (leave blank to keep unchanged): [/cyan]")
            if new_task:
                task['task'] = new_task

            while True:
                new_priority = console.input("[cyan]Set new priority (High/Medium/Low, leave blank to keep unchanged): [/cyan]").capitalize()
                if new_priority == "":
                    break  # Keep existing priority
                elif validate_priority(new_priority):
                    task['priority'] = new_priority
                    break
                else:
                    console.print("[red]Invalid priority! Please enter High, Medium, or Low.[/red]")

            while True:
                new_due_date = console.input("[cyan]Enter new due date (YYYY-MM-DD, leave blank to keep unchanged): [/cyan]")
                if new_due_date == "":
                    break  # Keep existing due date
                elif validate_date(new_due_date):
                    task['due_date'] = new_due_date
                    break
                else:
                    console.print("[red]Invalid date format! Please use YYYY-MM-DD.[/red]")

            console.print(f"[green]Task updated to: '{task['task']}' with priority '{task['priority']}' and due date '{task['due_date']}'[/green]")
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
        table.add_column("Due Date", justify="center", style="bold yellow")
        table.add_column("Status", justify="center", style="bold green")

        for index, task in enumerate(filtered_tasks, 1):
            status = "✅" if task.get('done') else "❌"
            table.add_row(str(index), task['task'], task['due_date'], status)

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
    console.print("- Use the menu to navigate and manage your tasks.")
    console.print("- You can add, edit, delete, mark tasks as done, and filter tasks.")
    console.print("- Follow prompts to enter the required information.")

# Main menu
def main_menu():
    load_tasks()
    console.print(ascii_art)
    while True:
        console.print("[bold cyan]1. Add Task[/bold cyan]")
        console.print("[bold cyan]2. Show Tasks[/bold cyan]")
        console.print("[bold cyan]3. Delete Task[/bold cyan]")
        console.print("[bold cyan]4. Mark Task as Done[/bold cyan]")
        console.print("[bold cyan]5. Edit Task[/bold cyan]")
        console.print("[bold cyan]6. Filter Tasks[/bold cyan]")
        console.print("[bold cyan]7. Show Task Summary[/bold cyan]")
        console.print("[bold cyan]8. Show Help[/bold cyan]")
        console.print("[bold cyan]9. Exit[/bold cyan]")

        choice = console.input("[cyan]Enter your choice: [/cyan]")
        
        if choice == '1':
            add_task()
        elif choice == '2':
            show_tasks()
        elif choice == '3':
            delete_task()
        elif choice == '4':
            mark_done()
        elif choice == '5':
            edit_task()
        elif choice == '6':
            filter_tasks()
        elif choice == '7':
            task_summary()
        elif choice == '8':
            show_help()
        elif choice == '9':
            save_tasks()
            console.print("[green]Goodbye![/green]")
            break
        else:
            console.print("[red]Invalid choice! Please try again.[/red]")

# Run the program
if __name__ == "__main__":
    main_menu()