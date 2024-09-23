import sqlite3
from datetime import datetime

DB_PATH = 'sunlab_access.db'

# Initialize the database
def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()

        # Create users table with 'password' column
        cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                            id TEXT PRIMARY KEY,
                            first_name TEXT,
                            last_name TEXT,
                            password TEXT,
                            status TEXT CHECK(status IN ('active', 'suspended'))
                        )''')

        # Create access logs table
        cursor.execute('''CREATE TABLE IF NOT EXISTS access_logs (
                            log_id INTEGER PRIMARY KEY AUTOINCREMENT,
                            student_id TEXT,
                            sign_in_time TEXT,
                            sign_out_time TEXT,
                            FOREIGN KEY (student_id) REFERENCES users(id)
                        )''')

        # Check if the admin user already exists, if not, insert default admin
        cursor.execute("SELECT * FROM users WHERE id = 'admin'")
        if cursor.fetchone() is None:
            # Insert the default admin user with id='admin' and password='admin'
            cursor.execute("INSERT INTO users (id, first_name, last_name, password, status) VALUES (?, ?, ?, ?, ?)",
                           ('admin', 'Admin', 'User', 'admin', 'active'))
            print("Admin user created with default credentials (admin/admin).")

        conn.commit()

# New function to get a user's status
def get_user_status(student_id):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT status FROM users WHERE id = ?", (student_id,))
        result = cursor.fetchone()
        return result[0] if result else None

# Check user credentials (admin login)
def check_credentials(username, password):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ? AND password = ?", (username, password))
        user = cursor.fetchone()
        return user is not None

# Add a new access record for sign-in
def add_access_record(student_id):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        sign_in_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute("INSERT INTO access_logs (student_id, sign_in_time) VALUES (?, ?)", (student_id, sign_in_time))
        conn.commit()

# Update the sign-out time for a student
def update_sign_out_time(student_id):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        sign_out_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute("UPDATE access_logs SET sign_out_time = ? WHERE student_id = ? AND sign_out_time IS NULL",
                       (sign_out_time, student_id))
        conn.commit()

# Check if the student is signed in (no sign_out_time yet)
def is_student_signed_in(student_id):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM access_logs WHERE student_id = ? AND sign_out_time IS NULL", (student_id,))
        return cursor.fetchone() is not None

# Retrieve all access records for history
def get_access_logs():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT student_id, sign_in_time, sign_out_time FROM access_logs")
        return cursor.fetchall()

# Activate or suspend a user (admin action)
def update_user_status(student_id, status):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET status = ? WHERE id = ?", (status, student_id))
        conn.commit()

# Check if the student is activated
def is_user_active(student_id):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT status FROM users WHERE id = ?", (student_id,))
        result = cursor.fetchone()
        return result and result[0] == 'active'

# Add a new student with first and last names
def add_new_student(student_id, first_name, last_name):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (id, first_name, last_name, password, status) VALUES (?, ?, ?, ?, ?)",
                       (student_id, first_name, last_name, None, 'active'))
        conn.commit()

# Get all users with their statuses, excluding the admin
def get_users():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, first_name, last_name, status FROM users WHERE id != 'admin'")
        return cursor.fetchall()

# Initialize the database at the start
init_db()
