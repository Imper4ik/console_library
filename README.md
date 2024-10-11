Book Library Management System
This is a Python-based application that allows users to manage a library of books. It provides features like user registration, login, adding, deleting, and displaying books. The system stores user and book information in a PostgreSQL database.

Features
  - User Registration
  - User Login
  - Add Book to User's Library
  - Remove Book from User's Library
  - View User's Books
  - View All Books in the Library

Project Structure
 The project consists of the following files:

 - book.py: Contains functions for managing book information, including adding, removing, and displaying books.
 - config.py: Contains configuration settings for connecting to the PostgreSQL database (such as host, username, password, and database name).
 - main.py: The main entry point of the application. It manages the user interface and interaction with the user.
 - sql_db.py: Handles database operations, such as inserting user information, verifying credentials, and interacting with the library and user book tables.
 - requirements: Lists the dependencies required for this project (like psycopg2, bcrypt).


Installation
 Prerequisites
  - Python 3.x
  - PostgreSQL installed and running
  - Python virtual environment (recommended)
  
Setup Instructions
 Clone the repository:
  git clone https://github.com/yourusername/book-library-system.git
  cd book-library-system

Install Dependencies:
 It's recommended to use a virtual environment. Run the following commands:

  python -m venv venv
  source venv/bin/activate  # On Windows use `venv\Scripts\activate`
  pip install -r requirements
  Set up PostgreSQL Database:

Ensure that PostgreSQL is installed, and create a new database for this application. For example:

  CREATE DATABASE book_library_db;
  Configure Database:

Update the config.py file with your PostgreSQL connection details:

  host = "your_host"
  user = "your_username"
  password = "your_password"
  dbname = "book_library_db"
  Run the Application:
  

After setting up the database and installing the dependencies, you can start the application by running:

  python main.py
  Database Setup:

When you first run the application, it will automatically create the necessary tables in the PostgreSQL database.

Usage
 When you run the application, you'll be prompted to choose from several options:
  Register a new user
  Log in to the system
  Add a book
  Delete a book
  View your books
  View all books in the library
  Exit the application
  
Dependencies
  psycopg2: Python PostgreSQL adapter
  bcrypt: For password hashing
  Additional dependencies can be found in the requirements file.
  
License
 This project is licensed under the MIT License. See the LICENSE file for details.

Note
  Make sure to replace the database credentials in config.py with your actual credentials.
  If you encounter any issues, ensure that PostgreSQL is properly configured and that the database is up and running.
