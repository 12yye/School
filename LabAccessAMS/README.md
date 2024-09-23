# SUN Lab Access System

## Overview

The **SUN Lab Access System** is a desktop application designed to manage and track student access to the Student Unix Network (SUN) Lab. It features both student and admin functionalities for signing in and managing user access.

## Features

- **Student Sign-In/Sign-Out**: Students can sign in and out using their student ID.
- **Admin Panel**: Admins can manage user access by activating, suspending, or reactivating users.
- **User Management**: Admins can create new users by entering their first and last names, along with their student ID.
- **View History**: Admins can view a table of all sign-in/sign-out events.

## Prerequisites

Before you begin, ensure you have the following installed:

- Python 3.12 or higher
- Tkinter (usually included with Python)
- SQLite (usually included with Python)

## Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/yourusername/SUNLabAccessSystem.git
   cd SUNLabAccessSystem
2. Install the required dependencies:
   pip install -r requirements.txt
3. Run the application:
   python main.py

Usage
Student Sign-In/Sign-Out
Step 1: Launch the app and enter your 9-digit student ID.
Step 2: Click Sign In/Out to log your entry or exit from the SUN Lab.
If your ID is not activated, you will receive an error message.

Admin Panel
Step 1: In the main window, click Admin Login.
Step 2: Enter the admin credentials. The default is:
Username: admin
Password: admin

Step 3: In the Admin Panel, you can:
Activate, suspend, or reactivate users.
View the sign-in/sign-out history.

Admin Functionalities:
Activate User: Add a new user with a student ID and their first and last names.
Suspend User: Temporarily suspend a user’s access.
Reactivate User: Restore a suspended user’s access.
View Logs: View the student sign-in and sign-out history.

Database
The application uses SQLite as its database system, and the sunlab_access.db file is automatically created when the program is run for the first time. This database stores user information and their sign-in/sign-out activity logs.

License
This project is licensed under the MIT License.
