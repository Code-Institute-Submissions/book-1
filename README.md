# To-Do List
**To-Do List** is a command-line interface (CLI) for a simple to-do list manager with user registration, login, and various task management functions. It utilizes JSON to store user data, bcrypt for password hashing, and Rich for styled CLI output. Key features include: i) *User Authentication*: Users can register or log in, with passwords stored securely in hashed form, ii) *Task Management*: Users can add, delete, edit, and mark tasks as done, iii) *Filtering and Searching*: Tasks can be filtered by priority or searched by keyword, iv) *Sorting*: Tasks can be sorted by due date for easy tracking, v) *Data Persistence*: User and task data are saved in a JSON file for data persistence across sessions. The program uses Rich library for enhanced CLI visuals and offers a menu-driven interface for ease of use. The main loop allows users to interact with tasks until they choose to log out or exit the program. This project appeals to anyone seeking a streamlined, code-driven way to stay organized and productive in a customizable, offline environment.

To test the application use the following user data to login:
- username: **evanthia**
- password: **123456**

The test user already contains a list of to-do tasks. Of course, you can also create a new user and add your own tasks.

[Link to live project](https://to-do-list-mgmt-80fbcde49609.herokuapp.com/)

![To-Do List](images/welcome.png)

 * [To-Do List](#to-do-list)
   * [Table of Contents](#table-of-contents)
   * [Introduction](#introduction)
       * [Description](#description)
       * [Purpose](#purpose)
       * [User Demographic](#user-demographic)
       * [Flowchart](#flowchart)
   * [Existing Features](#existing-features)
   * [Data Model](#data-model)
   * [Manual Testing](#manual-testing)
   * [Deployment](#deployment)
   * [Credits](#credits)

<!-- table of contents created by Adrian Bonnet, see https://github.com/Relex12/Markdown-Table-of-Contents for more -->
## Table of Contents

## Introduction

### Description
Here are the key features of this Python-based task manager (must-have):
- Task Management: Allow users to add, edit, delete, and mark tasks as done, keeping track of priority levels, due dates, and completion status.

- User Authentication and Data Security: Ensure data privacy and security by implementing a login system with secure password hashing. This allows multiple users to maintain separate task lists and prevents unauthorized access.

- Data Persistence: Enable data persistence across sessions using JSON, so users can retain their task lists between uses of the program.

- CLI-based Usability: Make the tool accessible from the command line with intuitive menu navigation, styled with Rich for an improved CLI experience.

### Purpose
The purpose of this project is to create a command-line task manager that enables users to manage their personal to-do lists with ease. Designed for simplicity and security, the application offers a robust feature set within a user-friendly interface. This tool is ideal for users who prefer a straightforward, text-based task manager and who value control over their task lists without relying on external applications or GUIs. It’s a foundational project for learning about user authentication, data management, and creating interactive command-line applications.

### User Demographic
The target audience for this Python-based task manager includes i) **Developers and Tech Enthusiasts**: Users comfortable with command-line interfaces who prefer minimalistic, non-GUI tools for personal productivity, ii) **Beginner Programmers**: Individuals looking to learn how to manage data, implement secure password hashing, and build interactive CLI applications in Python, iii) **Productivity-Focused Individuals**: People who enjoy organizing tasks and managing to-do lists, especially those who want a lightweight, distraction-free solution that doesn’t rely on complex software or internet access, iv) **Privacy-Conscious Users**: Users who prefer a personal, offline task manager without cloud dependencies, ensuring their task data stays on their device, and finally v) **Students and Educators**: Individuals in educational environments, where such a program can serve as a project to learn about user data handling, file I/O, and secure password management.

#### As a first time user, I'd like to:
- **Register**: create an account and log in.
- **Add Task**: create a to-do list with my upcoming tasks.
- **Organize**: save my tasks in the to-do list and be able to mark them as done according to date.
- **Access**: navigate my to-do tasks with an intuitive and visually appealing interface.
- **Manage**: view, search, edit, and delete tasks from the list with a keystroke.
- **Feed back**: get clear feedback from the application.
- **Experience**: enjoy a user-friendly program, even without any prior experience with terminal-based applications.

#### As a frequent user, I'd like to:
- **Authenticate**: access the application with passwords stored securely in the appropriate file.
- **Access**: retrieve quickly previously added to-do lists for efficient user interaction.
- **Manage**: streamline to-do list tasks with powerful batch editing and deletion features.
- **Personalize**: customize my experience by setting preferred task priority, due date, completion process.
- **Uncover**: handle large amounts of to-do list tasks that can be sorted by due date and priority level for easy tracking
- **Filter**: search effortlessly for specific tasks by keyword.
- **Upcycle**: focus on the program's reliability, responsiveness, and fast performance for all my to-do list tasks.

### Flowchart

The particular flowchart visually represents the sequence of steps, decisions, and processes involved before the development stage. I tried to break down complex processes into clear, manageable steps, making it easier to understand and follow. By mapping out each step, the graph helped me identify inefficiencies, redundancies, or potential problem areas in the workflow and the program logic. The relevant flowchart acts as blueprint, guiding the coding and debugging process and making it easier to maintain and update the system later. It also serves as documentation for how the program or the system works, which is helpful for future reference, onboarding new team members, or explaining the system to non-technical users. Additionally, I wanted to generate a graph that provides a common visual language for all stakeholders (developers, users, managers, etc.), facilitating clear communication about how a process works or how a program functions. 

To visualize the necessary steps to create the to-do list manager, I created the flowchart below using [Lucidchart](https://www.lucidchart.com/) in order to map out logic in decision-making, loops, input/output operations, and error handling, providing a clear overview before diving into coding.

![Flowchart](images/flowchart.jpeg)

## Existing Features

### Welcome screen
On the welcome screen, ASCII Art with the name of the application is displayed. Underneath the welcome message, the user can decide whether they want to register, login, or exit the program. The input is validated to be either 1, 2 or 3.

### Register
Users have to create an account in order to be able to store and view their to-do list tasks. A username and password have to be entered. After validation, they are stored in a .json file and the user is redirected to the Login. The username is validated to have at least 4 characters and is stored as all lowercase. Furthermore, the method ensures that the username is not taken. The password has to be at least 4 characters long as well. The user can enter exit the program instead of creating an account or logging in. 

### Login
A user that already created an account can log in by entering their username and password. The method validates the input by checking if the username exists in the users.json file and if the password that is entered is identical to the one stored. For security reasons, I used getpass to hide the input while typing in the password. The user should finish the process before he/she enters the main menu screen.

### Add Task

### Delete Task

### Mark Task

### Edit Task

### Show All Tasks

### Tasks by Priority

### Keyword Search

### Tasks by Due Date

### Logout

## Data Model

## Manual Testing

## Deployment

## Credits