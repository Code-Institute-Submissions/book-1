import gspread
from google.oauth2.service_account import Credentials
import json
import os
import bcrypt
import getpass
from rich.console import Console
from rich.table import Table
from datetime import datetime
    

# ASCII art
ascii_art = r'''
 /$$$$$$$$             /$$$$$$$               /$$       /$$             /$$    
|__  $$__/            | $$__  $$             | $$      |__/            | $$    
   | $$  /$$$$$$      | $$  \ $$  /$$$$$$    | $$       /$$  /$$$$$$$ /$$$$$$  
   | $$ /$$__  $$ /$$$| $$  | $$ /$$__  $$   | $$      | $$ /$$_____/|_  $$_/  
   | $$| $$  \ $$|___/| $$  | $$| $$  \ $$   | $$      | $$|  $$$$$$   | $$    
   | $$| $$  | $$     | $$  | $$| $$  | $$   | $$      | $$ \____  $$  | $$ /$$
   | $$|  $$$$$$/     | $$$$$$$/|  $$$$$$/   | $$$$$$$$| $$ /$$$$$$$/  |  $$$$/
   |__/ \______/      |_______/  \______/    |________/|__/|_______/    \___/  
'''


SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]


CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('to-do_list')

users = SHEET.worksheet("users")
data = users.get_all_values()
print(data)


# Initialize the rich console for styled output
console = Console()

# Define the filename for user data
USER_DATA_FILE = 'users.json'

# Load user data from JSON file
def load_users():
    """Load user data from a JSON file.

    Returns:
        dict: A dictionary containing user data. If the file is not found
              or cannot be decoded, returns an empty dictionary.
    """
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, 'r') as file:
            return json.load(file)
    return {}

# Save user data to JSON file
def save_users(users):
    """Save user data to a JSON file.

    Args:
        users (dict): A dictionary containing user data to be saved.

    Raises:
        IOError: If there is an error while saving the file.
    """
    with open(USER_DATA_FILE, 'w') as file:
        json.dump(users, file)

# User registration with password hashing
def register(users):
    """Register a new user.

    Args:
        users (dict): A dictionary containing existing users.

    Raises:
        ValueError: If the username already exists or is invalid.
    """
    while True:
        username = console.input("Enter a username: ").strip()
        if not username:
            console.print("[red]Username cannot be empty. Please enter a valid username.[/red]")
            continue

        if username in users:
            console.print("[red]Username already exists. Please choose another one.[/red]")
        else:
            while True:
                password = getpass.getpass("Enter a password: ").strip()
                if not password:
                    console.print("[red]Password cannot be empty. Please enter a valid password.[/red]")
                else:
                    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
                    users[username] = {'password': hashed_password.decode('utf-8'), 'tasks': []}
                    console.print(f"[green]User '{username}' registered successfully![/green]")
                    save_users(users)  # Save after registration
                    return

# User login with password verification
def login(users):
    """Log in an existing user.

    Args:
        users (dict): A dictionary containing existing users.

    Returns:
        str: The username of the logged-in user.
    
    Raises:
        ValueError: If the username or password is invalid.
    """
    while True:
        username = console.input("Enter your username: ")
        password = getpass.getpass("Enter your password: ").encode('utf-8')
        if username in users and bcrypt.checkpw(password, users[username]['password'].encode('utf-8')):
            console.print(f"[green]Welcome back, {username}![/green]")
            return username
        else:
            console.print("[red]Invalid username or password. Please try again.[/red]")

# Display tasks using a rich table
def show_tasks(tasks):
    """Display the user's tasks in a formatted table.

    Args:
        tasks (list): A list of tasks to display.
    """
    if not tasks:
        console.print("[yellow]Your to-do list is empty.[/yellow]")
        return

    table = Table(title="To-Do List", show_header=True, header_style="bold cyan")
    table.add_column("No.", justify="right", style="bold magenta", width=3)
    table.add_column("Task", justify="left", style="bold white")
    table.add_column("Priority", justify="center", style="bold blue")
    table.add_column("Due Date", justify="center", style="bold yellow")
    table.add_column("Status", justify="center", style="bold green")

    for index, task in enumerate(tasks, 1):
        status = "✅" if task.get('done') else "❌"
        due_date = task.get('due_date', 'N/A')
        table.add_row(str(index), task['task'], task['priority'], due_date, status)

    console.print(table)

# Add a task to the user's task list
def add_task(user_data):
    """Add a new task to the user's task list.

    Args:
        user_data (dict): A dictionary containing the user's data, including their tasks.
    """
    while True:
        task = console.input("[cyan]Enter the task you want to add (e.g., 'Buy groceries'): [/cyan]").strip()
        if not task:
            console.print("[red]Task name cannot be empty! Please enter a valid task.[/red]")
        else:
            break

    while True:
        priority = console.input("[cyan]Set priority (High/Medium/Low) [example: High]: [/cyan]").capitalize()
        if priority in ["High", "Medium", "Low"]:
            break
        else:
            console.print("[red]Invalid priority! Please enter High, Medium, or Low.[/red]")

    while True:
        due_date = console.input("[cyan]Enter due date (YYYY-MM-DD) [example: 2024-10-15]: [/cyan]")
        if validate_date(due_date):
            break
        else:
            console.print("[red]Invalid date format! Please use YYYY-MM-DD.[/red]")

    user_data['tasks'].append({'task': task, 'priority': priority, 'due_date': due_date, 'done': False})
    console.print(f"[green]Task '{task}' added successfully![/green]")
    save_users(users)  # Save after adding a task

# Validate the date input
def validate_date(date_text):
    """Validate the format of a date string.

    Args:
        date_text (str): The date string to validate.

    Returns:
        bool: True if the date is valid, False otherwise.
    """
    try:
        datetime.strptime(date_text, '%Y-%m-%d')
        return True
    except ValueError:
        return False

# Delete a task from the user's task list
def delete_task(user_data):
    """Delete a task from the user's task list.

    Args:
        user_data (dict): A dictionary containing the user's data, including their tasks.
    """
    show_tasks(user_data['tasks'])
    if not user_data['tasks']:
        return  # No tasks to delete

    while True:
        task_num = console.input("[cyan]Enter the task number to delete (e.g., '1'): [/cyan]")
        if task_num.isdigit() and 1 <= int(task_num) <= len(user_data['tasks']):
            removed_task = user_data['tasks'].pop(int(task_num) - 1)
            console.print(f"[green]Task '{removed_task['task']}' deleted successfully![/green]")
            save_users(users)  # Save after deleting a task
            break
        else:
            console.print("[red]Invalid task number! Please try again.[/red]")

# Mark a task as done
def mark_done(user_data):
    """Mark a task as done.

    Args:
        user_data (dict): A dictionary containing the user's data, including their tasks.
    """
    show_tasks(user_data['tasks'])
    if not user_data['tasks']:
        return  # No tasks to mark

    while True:
        task_num = console.input("[cyan]Enter the task number to mark as done (e.g., '1'): [/cyan]")
        if task_num.isdigit() and 1 <= int(task_num) <= len(user_data['tasks']):
            user_data['tasks'][int(task_num) - 1]['done'] = True
            console.print(f"[green]Task {task_num} marked as done successfully![/green]")
            save_users(users)  # Save after marking a task as done
            break
        else:
            console.print("[red]Invalid task number! Please try again.[/red]")

# Edit an existing task
def edit_task(user_data):
    """Edit an existing task in the user's task list.

    Args:
        user_data (dict): A dictionary containing the user's data, including their tasks.
    """
    show_tasks(user_data['tasks'])
    if not user_data['tasks']:
        return  # No tasks to edit

    while True:
        task_num = console.input("[cyan]Enter the task number to edit (e.g., '1'): [/cyan]")
        if task_num.isdigit() and 1 <= int(task_num) <= len(user_data['tasks']):
            task_index = int(task_num) - 1
            task = user_data['tasks'][task_index]

            console.print(f"[yellow]Editing Task: {task['task']} (Priority: {task['priority']}, Due Date: {task['due_date']})[/yellow]")
            new_task = console.input("[cyan]Enter the new task description (leave blank to keep unchanged): [/cyan]")
            if new_task:
                task['task'] = new_task

            while True:
                new_priority = console.input("[cyan]Set new priority (High/Medium/Low, leave blank to keep unchanged): [/cyan]").capitalize()
                if new_priority == "":
                    break  # Keep existing priority
                elif new_priority in ["High", "Medium", "Low"]:
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

            console.print(f"[green]Task updated successfully! New Details: '{task['task']}' (Priority: '{task['priority']}', Due Date: '{task['due_date']}')[/green]")
            save_users(users)  # Save after editing a task
            break
        else:
            console.print("[red]Invalid task number! Please try again.[/red]")

# Filter tasks by priority
def filter_tasks(user_data):
    """Filter tasks based on their priority level.
    This function prompts the user to enter a priority level (High, Medium, Low) and then
    filters the tasks that match the specified priority. The filtered tasks are displayed
    in a formatted table. If no tasks match the priority, a message is shown.
    
    Args:
        user_data (dict): A dictionary containing the user's data, including their tasks.
    """
    priority = console.input("[cyan]Enter priority to filter tasks (High/Medium/Low): [/cyan]").capitalize()
    if priority not in ["High", "Medium", "Low"]:
        console.print("[red]Invalid priority! Please enter High, Medium, or Low.[/red]")
        return

    filtered_tasks = [task for task in user_data['tasks'] if task['priority'] == priority]
    if filtered_tasks:
        console.print(f"[green]Tasks with '{priority}' priority:[/green]")
        show_tasks(filtered_tasks)
    else:
        console.print(f"[yellow]No tasks found with {priority} priority.[/yellow]")

# Search tasks by keyword
def search_tasks(user_data):
    """ Search tasks list for a specific keyword.
    This function is searching the task list according to a given keyword. If a user does not set a keyword 
    the function returns the whole list and counts the empty spaces.
    """
    keyword = console.input("[cyan]Enter keyword to search for tasks (e.g., 'groceries'): [/cyan]")
    found_tasks = [task for task in user_data['tasks'] if keyword.lower() in task['task'].lower()]

    if found_tasks:
        console.print(f"[green]Found {len(found_tasks)} tasks matching your search:[/green]")
        show_tasks(found_tasks)
    else:
        console.print("[yellow]No tasks found matching your search.[/yellow]")

# Sort tasks by due date
def sort_tasks_by_date(user_data):
    """Sort the user's tasks by their due date.

    This function sorts the tasks by the due date in ascending order. If a task has 'N/A' as the due date, 
    it is treated as the maximum possible date for sorting purposes.

    Args:
        user_data (dict): A dictionary containing the user's data, including their tasks.
    """
    try:
        user_data['tasks'].sort(key=lambda task: datetime.strptime(task['due_date'], '%Y-%m-%d') if task['due_date'] != 'N/A' else datetime.max)
        console.print("[green]Tasks sorted by due date successfully![/green]")
    except ValueError:
        console.print("[red]Error sorting tasks. Some tasks may have invalid dates.[/red]")


def clear_screen():
    """Clear the terminal screen.

    This function clears the terminal screen for a cleaner interface,
    taking into account different operating systems.

    """
    os.system('clear')  # For Linux/macOS
    # os.system('cls')  # Use this for Windows    

# Main program loop
def main():
    """Run the task manager application.

    This function handles user registration, login, and task management.
    """
    global users  # Use global variable to access users in nested functions
    users = load_users()
    console.print(ascii_art)

    while True:
        console.print("[bold cyan]1. Register[/bold cyan]")
        console.print("[bold cyan]2. Login[/bold cyan]")
        console.print("[bold cyan]3. Exit[/bold cyan]")
        choice = console.input("[cyan]Choose an option (1-3): [/cyan]")
        clear_screen()
        if choice == "1":
            register(users)
        elif choice == "2":
            username = login(users)
            user_data = users[username]  # Retrieve the logged-in user's data

            while True:
                console.print("[bold cyan]1. Add Task[/bold cyan]")
                console.print("[bold cyan]2. Delete Task[/bold cyan]")
                console.print("[bold cyan]3. Mark Task[/bold cyan]")
                console.print("[bold cyan]4. Edit Task[/bold cyan]")
                console.print("[bold cyan]5. Show All Tasks[/bold cyan]")
                console.print("[bold cyan]6. Tasks by Priority[/bold cyan]")
                console.print("[bold cyan]7. Keyword Search[/bold cyan]")
                console.print("[bold cyan]8. Tasks by Due Date[/bold cyan]")
                console.print("[bold cyan]9. Logout[/bold cyan]")
                user_choice = console.input("[cyan]Choose an option (1-9): [/cyan]")
                clear_screen()
                if user_choice == "1":
                    add_task(user_data)
                    clear_screen()
                elif user_choice == "2":
                    delete_task(user_data)
                    clear_screen()
                elif user_choice == "3":
                    mark_done(user_data)
                    clear_screen()
                elif user_choice == "4":
                    edit_task(user_data)
                    clear_screen()
                elif user_choice == "5":
                    show_tasks(user_data['tasks'])
            
                elif user_choice == "6":
                    filter_tasks(user_data)
                    
                elif user_choice == "7":
                    search_tasks(user_data)
                    
                elif user_choice == "8":
                    sort_tasks_by_date(user_data)
                    console.print("[green]Tasks sorted by due date successfully![/green]")
                    clear_screen()
                    show_tasks(user_data['tasks'])
                    
                elif user_choice == "9":
                    console.print("[green]Logging out...[/green]")
                    break
                else:
                    console.print("[red]Invalid choice! Please choose a number between 1 and 9.[/red]")
        elif choice == "3":
            console.print("[green]Exiting the program.[/green]")
            break
        else:
            console.print("[red]Invalid choice! Please choose a number between 1 and 3.[/red]")

if __name__ == "__main__":
    main()