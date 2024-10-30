import json
import os
import bcrypt
import getpass
from rich.console import Console
from rich.table import Table
from datetime import datetime

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

console = Console()

USER_DATA_FILE = 'users.json'


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


def save_users(users):
    """Save user data to a JSON file.

    Args:
        users (dict): A dictionary containing user data to be saved.

    Raises:
        IOError: If there is an error while saving the file.
    """
    with open(USER_DATA_FILE, 'w') as file:
        json.dump(users, file)


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
            console.print(
                f"""[red]
Username cannot be empty. Please enter a valid username.[/red]"""
            )
        elif len(username) < 4:
            console.print(
                f"""[red]
Username must be at least 4 characters long. Please try again.[/red]"""
            )
        elif username in users:
            console.print(
                f"""[red]
Username already exists. Please choose another one.[/red]"""
            )
        else:
            while True:
                password = getpass.getpass("Enter a password: ").strip()
                if not password:
                    console.print(
                        f"""[red]
Password cannot be empty. Please enter a valid password.[/red]"""
                    )
                elif len(password) < 4:
                    console.print(
                        f"""[red]
Password must be at least 4 characters long. Please try again.[/red]"""
                    )
                else:
                    hashed_password = bcrypt.hashpw(
                        password.encode('utf-8'), bcrypt.gensalt()
                    )
                    users[username] = {
                        'password': hashed_password.decode('utf-8'),
                        'tasks': []
                    }
                    console.print(
                        f"""[green]
User '{username}' registered successfully![/green]"""
                    )
                    save_users(users)  # Save after registration
                    return


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
        username = console.input("Enter your username: ").strip()
        if len(username) < 4:
            console.print(
                f""""[red]
Username must be at least 4 characters long. Please try again.[/red]"""
            )
            continue

        password = getpass.getpass("Enter your password: ").strip()
        if len(password) < 4:
            console.print(
                f"""[red]
Password must be at least 4 characters long. Please try again.[/red]"""
            )
            continue

        if username in users and bcrypt.checkpw(
                password.encode('utf-8'),
                users[username]['password'].encode('utf-8')
        ):
            console.print(f"[green]Welcome back, {username}![/green]")
            return username
        else:
            console.print(
                f"""[red]
Invalid username or password. Please try again.[/red]"""
            )


def show_tasks(tasks):
    """Display the user's tasks in a formatted table.

    Args:
        tasks (list): A list of tasks to display.
    """
    if not tasks:
        console.print("[yellow]Your to-do list is empty.[/yellow]")
        return

    table = Table(
        title="To-Do List", show_header=True, header_style="bold cyan"
    )
    table.add_column("No.", justify="right", style="bold magenta", width=3)
    table.add_column("Task", justify="left", style="bold white")
    table.add_column("Priority", justify="center", style="bold blue")
    table.add_column("Due Date", justify="center", style="bold yellow")
    table.add_column("Status", justify="center", style="bold green")

    for index, task in enumerate(tasks, 1):
        status = "✅" if task.get('done') else "❌"
        due_date = task.get('due_date', 'N/A')
        table.add_row(
            str(index), task['task'], task['priority'], due_date, status
        )

    console.print(table)


def add_task(user_data):
    """Add a new task to the user's task list.

    Args:
        user_data (dict):
        A dictionary containing the user's data, including their tasks.
    """
    while True:
        task = console.input(
            f"""[cyan]
            Enter the task you want to add
            (e.g., 'Buy groceries'): [/cyan]"""
        ).strip()
        # Check if the input contains only alphabetic characters and spaces
        if not task or not task.replace(' ', '').isalpha():
            console.print(
                f"""[red]
Task name can only contain alphabetic characters and cannot be empty!
Please enter a valid task.[/red]"""
            )
        else:
            break

    while True:
        priority = console.input(
            f"""[cyan]
Set priority (High/Medium/Low) [example: High]: [/cyan]"""
        ).capitalize()
        if priority in ["High", "Medium", "Low"]:
            break
        else:
            console.print(
                f"""[red]
Invalid priority! Please enter High, Medium, or Low.[/red]"""
            )

    while True:
        due_date = console.input(
            f"""[cyan]
Enter due date (YYYY-MM-DD) [example: 2024-10-15]: [/cyan]"""
        )
        if validate_date(due_date):
            break
        else:
            console.print(
                f"""[red
Invalid date format! Please use YYYY-MM-DD.[/red]"""
            )

    user_data['tasks'].append(
        {
            'task': task,
            'priority': priority,
            'due_date': due_date,
            'done': False
        }
    )
    console.print(f"[green]Task '{task}' added successfully![/green]")
    save_users(users)  # Save after adding a task


def validate_date(date_text):
    """
    Validate the format of a date string and ensure it is not in the past.

    Args:
        date_text (str): The date string to validate.

    Returns:
        bool: True if the date is valid and not in the past, False otherwise.
    """
    try:
        # Parse the date and get the current date
        input_date = datetime.strptime(date_text, '%Y-%m-%d')
        today = datetime.today()

        # Check if the input date is before today's date
        if input_date.date() < today.date():
            console.print(
                f"""[red]
Date cannot be in the past!
Please enter a valid present or future date.[/red]"""
            )
            return False
        return True
    except ValueError:
        console.print("[red]Invalid date format! Please use YYYY-MM-DD.[/red]")
        return False


def delete_task(user_data):
    """Delete a task from the user's task list.

    Args:
        user_data (dict):
        A dictionary containing the user's data, including their tasks.
    """
    # Check if the user has any tasks
    if not user_data.get('tasks'):
        console.print(
            f"""[yellow]
No tasks available to delete. Please Add a task![/yellow]"""
        )
        return  # Exit if there are no tasks to delete

    show_tasks(user_data['tasks'])  # Display existing tasks for selection

    # Prompt the user to enter the task number to delete
    while True:
        task_num = console.input(
            f"""[cyan]
Enter the task number to delete (or type 'back' to cancel): [/cyan]"""
        ).strip()

        # Allow the user to go back without deleting
        if task_num.lower() == 'back':
            console.print("[yellow]Delete task operation cancelled.[/yellow]")
            return

        # Validate task number input
        if task_num.isdigit() and 1 <= int(
                task_num
            ) <= len(
                user_data['tasks']
        ):
            # Perform task deletion
            removed_task = user_data['tasks'].pop(int(task_num) - 1)
            console.print(
                f"""[green]
Task '{removed_task['task']}' deleted successfully![/green]"""
            )
            save_users(users)  # Save after deleting a task
            break
        else:
            console.print(
                f"""[red]
Invalid task number! Please try again or type 'back' to cancel.[/red]"""
            )


def mark_done(user_data):
    """Mark a task as done.

    Args:
        user_data (dict):
        A dictionary containing the user's data, including their tasks.
    """
    # Check if there are tasks to mark as done
    if not user_data.get('tasks'):
        console.print(
            f"""[yellow]
No tasks available to mark as done. Please add a task first![/yellow]"""
        )
        return  # Exit if there are no tasks to mark

    show_tasks(user_data['tasks'])  # Display existing tasks for selection

    while True:
        task_num = console.input(
            f"""[cyan]
Enter the task number to mark as done (or type 'back' to cancel): [/cyan]"""
        ).strip()

        # Allow the user to go back without marking
        if task_num.lower() == 'back':
            console.print("[yellow]Mark task operation cancelled.[/yellow]")
            return

        # Validate task number input
        if task_num.isdigit() and 1 <= int(
            task_num
        ) <= len(
            user_data['tasks']
        ):
            # Mark the task as done
            user_data['tasks'][int(task_num) - 1]['done'] = True
            console.print(
                f"""[green]
Task '{user_data['tasks'][int(task_num) - 1]['task']}'
marked as done successfully![/green]"""
            )
            save_users(users)  # Save after marking a task as done
            break
        else:
            console.print(
                f"""[red]
Invalid task number! Please try again or type 'back' to cancel.[/red]"""
            )


def edit_task(user_data):
    """Edit an existing task in the user's task list.

    Args:
        user_data (dict):
        A dictionary containing the user's data, including their tasks.
    """
    if not user_data['tasks']:
        console.print(
            f"""[yellow]
No tasks to edit. Please add a task first.[/yellow]"""
        )
        return

    # Display tasks in a table format
    table = Table(title="Task List")

    table.add_column("No.", justify="center", style="cyan", no_wrap=True)
    table.add_column("Task", style="magenta")
    table.add_column("Priority", justify="center", style="green")
    table.add_column("Due Date", justify="center", style="yellow")

    for idx, task in enumerate(user_data['tasks'], 1):
        table.add_row(
            str(idx), task['task'], task['priority'], task['due_date']
        )

    console.print(table)

    # Select the task to edit
    while True:
        try:
            task_num = int(console.input(
                f"""[cyan]
Enter the task number you want to edit: [/cyan]"""
            ))
            if 1 <= task_num <= len(user_data['tasks']):
                selected_task = user_data['tasks'][task_num - 1]
                break
            else:
                console.print(
                    f"""[red]
Invalid task number! Please enter a valid task number.[/red]"""
                )
        except ValueError:
            console.print("[red]Please enter a valid number.[/red]")

    # Update task name
    while True:
        new_task_name = console.input(
            f"""[cyan]
Enter new name for the task '{selected_task['task']}': [/cyan]"""
        ).strip()
        if not new_task_name or not new_task_name.replace(' ', '').isalpha():
            console.print(
                f"""[red]
Task name cannot be blank, contain numbers, or special characters!
Only alphabetic characters allowed.[/red]"""
            )
        else:
            selected_task['task'] = new_task_name
            break

    # Update priority
    while True:
        new_priority = console.input(
            f"""[cyan]
Set new priority (High/Medium/Low): [/cyan]"""
        ).capitalize()
        if new_priority in ["High", "Medium", "Low"]:
            selected_task['priority'] = new_priority
            break
        else:
            console.print(
                f"""[red]
Invalid priority! Please enter High, Medium, or Low.[/red]"""
            )

    # Update due date
    while True:
        new_due_date = console.input(
            f"""[cyan]Enter new due date (YYYY-MM-DD): [/cyan]"""
        )
        if validate_date(new_due_date):
            selected_task['due_date'] = new_due_date
            break
        else:
            console.print(
                f"""[red]Invalid date format! Please use YYYY-MM-DD.[/red]"""
            )

    console.print(
        f"""[green]
Task '{selected_task['task']}' updated successfully![/green]"""
    )
    save_users(users)  # Save after editing a task


def filter_tasks(user_data):
    """Filter tasks based on a specified priority
    and display them in a table format.

    Args:
        user_data (dict):
        A dictionary containing the user's data, including their tasks.
    """
    # Check if there are tasks available
    if not user_data['tasks']:
        console.print("[yellow]No tasks available to filter.[/yellow]")
        return

    # Prompt user for priority to filter tasks
    priority = console.input(
        f"""[cyan]Enter priority to filter tasks (High/Medium/Low): [/cyan]"""
    ).capitalize()
    if priority not in ["High", "Medium", "Low"]:
        console.print(
            f"""[red]
Invalid priority! Please enter High, Medium, or Low.[/red]"""
        )
        return

    # Filter tasks by priority
    filtered_tasks = [
        task for task in user_data['tasks'] if task['priority'] == priority
    ]

    if not filtered_tasks:
        console.print(
            f"""[yellow]No tasks found with '{priority}' priority.[/yellow]"""
        )
        return

    # Display filtered tasks in a table format
    table = Table(title=f"Tasks with '{priority}' Priority")

    table.add_column("No.", justify="center", style="cyan", no_wrap=True)
    table.add_column("Task", style="magenta")
    table.add_column("Priority", justify="center", style="green")
    table.add_column("Due Date", justify="center", style="yellow")

    for idx, task in enumerate(filtered_tasks, 1):
        table.add_row(
            str(idx), task['task'], task['priority'], task['due_date']
        )

    console.print(table)


def search_tasks(user_data):
    """Search tasks based on a keyword and
    display matching tasks in a table format.

    Args:
        user_data (dict): A dictionary containing the user's data,
        including their tasks.
    """
    # Check if there are tasks available
    if not user_data['tasks']:
        console.print("[yellow]No tasks available to search.[/yellow]")
        return

    # Prompt user for a search keyword
    keyword = console.input(
        f"""[cyan]Enter keyword to search tasks: [/cyan]"""
    ).strip()
    if not keyword:
        console.print("[red]Keyword cannot be blank.[/red]")
        return

    # Filter tasks by keyword
    matching_tasks = [
        task for task in user_data[
            'tasks'
        ] if keyword.lower() in task[
            'task'
        ].lower()
    ]

    if not matching_tasks:
        console.print(f"[yellow]No tasks found matching '{keyword}'.[/yellow]")
        return

    # Display matching tasks in a table format
    table = Table(title=f"Tasks Matching '{keyword}'")

    table.add_column("No.", justify="center", style="cyan", no_wrap=True)
    table.add_column("Task", style="magenta")
    table.add_column("Priority", justify="center", style="green")
    table.add_column("Due Date", justify="center", style="yellow")

    for idx, task in enumerate(matching_tasks, 1):
        table.add_row(
            str(idx), task['task'], task['priority'], task['due_date']
        )

    console.print(table)


def sort_tasks_by_date(user_data):
    """Sort the user's tasks by their due date.

    This function sorts the tasks by the due date in ascending order.
    If a task has 'N/A' as the due date,
    it is treated as the maximum possible date for sorting purposes.

    Args:
        user_data (dict): A dictionary containing the user's data,
        including their tasks.
    """
    try:
        user_data['tasks'].sort(
            key=lambda task: datetime.strptime(
                task['due_date'], '%Y-%m-%d'
            ) if task['due_date'] != 'N/A' else datetime.max
        )
        console.print("[green]Tasks sorted by due date successfully![/green]")
    except ValueError:
        console.print(
            f"""[red]
Error sorting tasks. Some tasks may have invalid dates.[/red]"""
        )


def clear_screen():
    """Clear the terminal screen.

    This function clears the terminal screen for a cleaner interface,
    taking into account different operating systems.

    """
    os.system('clear')  # For Linux/macOS
    # os.system('cls')  # Use this for Windows


def main():
    """Run the task manager application.

    This function handles user registration, login, and task management.
    """
    global users  # Use global variable to access users in nested functions
    users = load_users()
    console.print(ascii_art)

    while True:
        console.print("[cyan]Do you have an account?[cyan]")
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
                console.print("[cyan]To-Do List Main Menu:[cyan]")
                console.print("[bold cyan]1. Add Task[/bold cyan]")
                console.print("[bold cyan]2. Delete Task[/bold cyan]")
                console.print("[bold cyan]3. Mark Task[/bold cyan]")
                console.print("[bold cyan]4. Edit Task[/bold cyan]")
                console.print("[bold cyan]5. Show All Tasks[/bold cyan]")
                console.print("[bold cyan]6. Tasks by Priority[/bold cyan]")
                console.print("[bold cyan]7. Keyword Search[/bold cyan]")
                console.print("[bold cyan]8. Tasks by Due Date[/bold cyan]")
                console.print("[bold cyan]9. Logout[/bold cyan]")
                user_choice = console.input(
                    f"""[cyan]Choose an option (1-9): [/cyan]"""
                )
                clear_screen()
                if user_choice == "1":
                    add_task(user_data)
                    clear_screen()
                elif user_choice == "2":
                    delete_task(user_data)
                elif user_choice == "3":
                    mark_done(user_data)
                elif user_choice == "4":
                    edit_task(user_data)
                elif user_choice == "5":
                    show_tasks(user_data['tasks'])
                elif user_choice == "6":
                    filter_tasks(user_data)
                elif user_choice == "7":
                    search_tasks(user_data)
                elif user_choice == "8":
                    sort_tasks_by_date(user_data)
                    console.print(
                        f"""[green]
Tasks sorted by due date successfully![/green]"""
                    )
                    clear_screen()
                    show_tasks(user_data['tasks'])
                elif user_choice == "9":
                    console.print(
                        f"""[green]You successfully logged out...[/green]"""
                    )
                    break
                else:
                    console.print(
                        f"""[red]
Invalid choice! Please choose a number between 1 and 9.[/red]"""
                    )
        elif choice == "3":
            console.print("[green]Exiting the program.[/green]")
            break
        else:
            console.print(
                f"""[red]
Invalid choice! Please choose a number between 1 and 3.[/red]"""
            )


if __name__ == "__main__":
    main()
