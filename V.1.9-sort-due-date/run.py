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
def show_tasks(tasks_to_display=None):
    if tasks_to_display is None:
        tasks_to_display = tasks
        
    if not tasks_to_display:
        console.print("[yellow]Your to-do list is empty.[/yellow]")
    else:
        table = Table(title="To-Do List", show_header=True, header_style="bold cyan")
        table.add_column("No.", justify="right", style="bold magenta", width=3)
        table.add_column("Task", justify="left", style="bold white")
        table.add_column("Priority", justify="center", style="bold blue")
        table.add_column("Due Date", justify="center", style="bold yellow")
        table.add_column("Status", justify="center", style="bold green")

        for index, task in enumerate(tasks_to_display, 1):
            status = "✅" if task.get('done') else "❌"
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
    task = console.input("[cyan]Enter the task you want to add (e.g., 'Buy groceries'): [/cyan]")
    while True:
        priority = console.input("[cyan]Set priority (High/Medium/Low) [example: High]: [/cyan]").capitalize()
        if validate_priority(priority):
            break
        else:
            console.print("[red]Invalid priority! Please enter High, Medium, or Low.[/red]")

    # Get due date
    while True:
        due_date = console.input("[cyan]Enter due date (YYYY-MM-DD) [example: 2024-10-15]: [/cyan]")
        if validate_date(due_date):
            break
        else:
            console.print("[red]Invalid date format! Please use YYYY-MM-DD.[/red]")

    tasks.append({'task': task, 'priority': priority, 'due_date': due_date, 'done': False})
    console.print(f"[green]Task '{task}' added successfully![/green]")
    console.print(f"[green]Details: Priority - '{priority}', Due Date - '{due_date}'[/green]")

# Delete a task from the list
def delete_task():
    show_tasks()
    if not tasks:
        return  # No tasks to delete

    while True:
        task_num = console.input("[cyan]Enter the task number to delete (e.g., '1'): [/cyan]")
        if task_num.isdigit() and 1 <= int(task_num) <= len(tasks):
            removed_task = tasks.pop(int(task_num) - 1)
            console.print(f"[green]Task '{removed_task['task']}' deleted successfully![/green]")
            break
        else:
            console.print("[red]Invalid task number! Please try again.[/red]")

# Mark a task as done
def mark_done():
    show_tasks()
    if not tasks:
        return  # No tasks to mark

    while True:
        task_num = console.input("[cyan]Enter the task number to mark as done (e.g., '1'): [/cyan]")
        if task_num.isdigit() and 1 <= int(task_num) <= len(tasks):
            tasks[int(task_num) - 1]['done'] = True
            console.print(f"[green]Task {task_num} marked as done successfully![/green]")
            break
        else:
            console.print("[red]Invalid task number! Please try again.[/red]")

# Edit an existing task
def edit_task():
    show_tasks()
    if not tasks:
        return  # No tasks to edit

    while True:
        task_num = console.input("[cyan]Enter the task number to edit (e.g., '1'): [/cyan]")
        if task_num.isdigit() and 1 <= int(task_num) <= len(tasks):
            task_index = int(task_num) - 1
            task = tasks[task_index]
            
            console.print(f"[yellow]Editing Task: {task['task']} (Priority: {task['priority']}, Due Date: {task['due_date']})[/yellow]")
            new_task = console.input("[cyan]Enter the new task description (leave blank to keep unchanged) [example: 'Buy milk']: [/cyan]")
            if new_task:
                task['task'] = new_task

            while True:
                new_priority = console.input("[cyan]Set new priority (High/Medium/Low, leave blank to keep unchanged) [example: Medium]: [/cyan]").capitalize()
                if new_priority == "":
                    break  # Keep existing priority
                elif validate_priority(new_priority):
                    task['priority'] = new_priority
                    break
                else:
                    console.print("[red]Invalid priority! Please enter High, Medium, or Low.[/red]")

            while True:
                new_due_date = console.input("[cyan]Enter new due date (YYYY-MM-DD, leave blank to keep unchanged) [example: 2024-10-15]: [/cyan]")
                if new_due_date == "":
                    break  # Keep existing due date
                elif validate_date(new_due_date):
                    task['due_date'] = new_due_date
                    break
                else:
                    console.print("[red]Invalid date format! Please use YYYY-MM-DD.[/red]")

            console.print(f"[green]Task updated successfully! New Details: '{task['task']}' (Priority: '{task['priority']}', Due Date: '{task['due_date']}')[/green]")
            break
        else:
            console.print("[red]Invalid task number! Please try again.[/red]")

# Filter tasks by priority
def filter_tasks():
    while True:
        priority = console.input("[cyan]Enter priority to filter tasks (High/Medium/Low) [example: High]: [/cyan]").capitalize()
        if validate_priority(priority):
            break
        else:
            console.print("[red]Invalid priority! Please enter High, Medium, or Low.[/red]")

    filtered_tasks = [task for task in tasks if task['priority'] == priority]
    if filtered_tasks:
        console.print(f"[green]Filtered {len(filtered_tasks)} tasks with '{priority}' priority:[/green]")
        show_tasks(filtered_tasks)
    else:
        console.print(f"[yellow]No tasks found with {priority} priority.[/yellow]")

# Search tasks by keyword
def search_tasks():
    keyword = console.input("[cyan]Enter keyword to search for tasks (e.g., 'groceries'): [/cyan]")
    found_tasks = [task for task in tasks if keyword.lower() in task['task'].lower()]

    if found_tasks:
        console.print(f"[green]Found {len(found_tasks)} tasks matching your search:[/green]")
        show_tasks(found_tasks)
    else:
        console.print("[yellow]No tasks found matching your search.[/yellow]")

# Sort tasks by due date
def sort_tasks_by_date():
    global tasks
    tasks.sort(key=lambda task: datetime.strptime(task['due_date'], '%Y-%m-%d'))

# Main program loop
def main():
    load_tasks()
    console.print(ascii_art)
    while True:
        console.print("[bold cyan]1. Add Task[/bold cyan]")
        console.print("[bold cyan]2. Delete Task[/bold cyan]")
        console.print("[bold cyan]3. Mark Task as Done[/bold cyan]")
        console.print("[bold cyan]4. Edit Task[/bold cyan]")
        console.print("[bold cyan]5. Show All Tasks[/bold cyan]")
        console.print("[bold cyan]6. Filter Tasks by Priority[/bold cyan]")
        console.print("[bold cyan]7. Search Tasks[/bold cyan]")
        console.print("[bold cyan]8. Sort Tasks by Due Date[/bold cyan]")
        console.print("[bold cyan]9. Exit[/bold cyan]")

        choice = console.input("[cyan]Choose an option (1-9): [/cyan]")
        if choice == "1":
            add_task()
        elif choice == "2":
            delete_task()
        elif choice == "3":
            mark_done()
        elif choice == "4":
            edit_task()
        elif choice == "5":
            show_tasks()
        elif choice == "6":
            filter_tasks()
        elif choice == "7":
            search_tasks()
        elif choice == "8":
            sort_tasks_by_date()
            console.print("[green]Tasks sorted by due date successfully![/green]")
            show_tasks()
        elif choice == "9":
            save_tasks()
            console.print("[green]Tasks saved. Exiting the program.[/green]")
            break
        else:
            console.print("[red]Invalid choice! Please choose a number between 1 and 9.[/red]")

if __name__ == "__main__":
    main()