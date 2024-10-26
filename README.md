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
   * [Existing Features](#existing-features)
   * [Data Model](#data-model)
   * [Manual Testing](#manual-testing)
   * [Deployment](#deployment)
   * [Credits](#credits)

<!-- table of contents created by Adrian Bonnet, see https://github.com/Relex12/Markdown-Table-of-Contents for more -->
## Table of Contents

## Introduction

### Description
- Task Management: Allow users to add, edit, delete, and mark tasks as done, keeping track of priority levels, due dates, and completion status.

- User Authentication and Data Security: Ensure data privacy and security by implementing a login system with secure password hashing. This allows multiple users to maintain separate task lists and prevents unauthorized access.

- Data Persistence: Enable data persistence across sessions using JSON, so users can retain their task lists between uses of the program.

- CLI-based Usability: Make the tool accessible from the command line with intuitive menu navigation, styled with Rich for an improved CLI experience.

### Purpose
The purpose of this project is to create a command-line task manager that enables users to manage their personal to-do lists with ease. Designed for simplicity and security, the application offers a robust feature set within a user-friendly interface. This tool is ideal for users who prefer a straightforward, text-based task manager and who value control over their task lists without relying on external applications or GUIs. It’s a foundational project for learning about user authentication, data management, and creating interactive command-line applications.

### User Demographic
The target audience for this Python-based task manager includes: 
- Developers and Tech Enthusiasts: Users comfortable with command-line interfaces who prefer minimalistic, non-GUI tools for personal productivity.
- Beginner Programmers: Individuals looking to learn how to manage data, implement secure password hashing, and build interactive CLI applications in Python.
- Productivity-Focused Individuals: People who enjoy organizing tasks and managing to-do lists, especially those who want a lightweight, distraction-free solution that doesn’t rely on complex software or internet access.
- Privacy-Conscious Users: Users who prefer a personal, offline task manager without cloud dependencies, ensuring their task data stays on their device.
- Students and Educators: Individuals in educational environments, where such a program can serve as a project to learn about user data handling, file I/O, and secure password management.



## Existing Features

## Data Model

## Manual Testing

## Deployment

## Credits