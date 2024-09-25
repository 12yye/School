import tkinter as tk
from tkinter import messagebox, ttk
from database import add_access_record, update_sign_out_time, is_student_signed_in, is_user_active, \
    get_access_logs, get_users, update_user_status, check_credentials, add_new_student, get_user_status, \
    search_by_student_id, get_access_logs_for_student, search_by_date_range


# Style the application
def apply_styles():
    style = ttk.Style()
    style.theme_use('clam')

    # Style for buttons
    style.configure("TButton",
                    font=("Helvetica", 12, "bold"),
                    padding=10,
                    background="#5A9",
                    foreground="white",
                    focuscolor="",
                    borderwidth=2)

    # Style for labels
    style.configure("TLabel",
                    font=("Helvetica", 12),
                    padding=5,
                    foreground="#333")

    # Style for entry fields
    style.configure("TEntry",
                    font=("Helvetica", 12),
                    padding=5,
                    fieldbackground="white",
                    borderwidth=2,
                    relief="solid")

    # Style for Treeview (table)
    style.configure("Treeview",
                    font=("Helvetica", 12),
                    rowheight=25,
                    padding=5,
                    fieldbackground="white")
    style.configure("Treeview.Heading",
                    font=("Helvetica", 12, "bold"),
                    background="#5A9",
                    foreground="white",
                    padding=10)

# Placeholder functionality for ttk.Entry widget without 'fg' support
def add_placeholder(entry, placeholder_text):
    entry.insert(0, placeholder_text)

    def on_focus_in(event):
        if entry.get() == placeholder_text:
            entry.delete(0, tk.END)

    def on_focus_out(event):
        if entry.get() == '':
            entry.insert(0, placeholder_text)

    entry.bind('<FocusIn>', on_focus_in)
    entry.bind('<FocusOut>', on_focus_out)

# Regular window for students to sign in/out
def open_regular_window():
    window = tk.Tk()
    window.title("SUN Lab Access System")
    window.geometry("600x400")

    apply_styles()

    def sign_in_out():
        student_id = entry_student_id.get().strip()

        # Check if the student ID is 9 digits long
        if not student_id.isdigit() or len(student_id) != 9:
            messagebox.showerror("Error", "Student ID must be exactly 9 digits.")
            return

        # Check if the user is suspended or not activated
        status = get_user_status(student_id)
        if status == 'suspended':
            messagebox.showerror("Error", "The user has been suspended.")
            return
        elif status is None:
            messagebox.showerror("Error", "Student is not activated.")
            return

        if is_student_signed_in(student_id):
            update_sign_out_time(student_id)
            messagebox.showinfo("Sign Out", f"Student {student_id} signed out successfully.")
        else:
            add_access_record(student_id)
            messagebox.showinfo("Sign In", f"Student {student_id} signed in successfully.")

        refresh_history_table()

    def refresh_history_table():
        for row in history_table.get_children():
            history_table.delete(row)
        for log in get_access_logs():
            history_table.insert('', 'end', values=log)

    # UI for sign-in/out and history
    label_student_id = ttk.Label(window, text="Enter Student ID:")
    label_student_id.pack(pady=5)
    entry_student_id = ttk.Entry(window)
    entry_student_id.pack(pady=5)
    add_placeholder(entry_student_id, "Enter Student ID")

    button_sign_in_out = ttk.Button(window, text="Sign In/Out", command=sign_in_out)
    button_sign_in_out.pack(pady=10)

    # History table
    history_table = ttk.Treeview(window, columns=("Student ID", "Sign In Time", "Sign Out Time"), show='headings')
    history_table.heading("Student ID", text="Student ID")
    history_table.heading("Sign In Time", text="Sign In Time")
    history_table.heading("Sign Out Time", text="Sign Out Time")
    history_table.pack(fill=tk.BOTH, expand=True)

    refresh_history_table()

    # Admin access
    admin_button = ttk.Button(window, text="Admin Login", command=open_admin_login_window)
    admin_button.pack(pady=10)

    window.mainloop()

# Admin login window
def open_admin_login_window():
    login_window = tk.Toplevel()
    login_window.title("Admin Login")
    login_window.geometry("300x200")

    apply_styles()

    def attempt_login():
        username = entry_username.get().strip()
        password = entry_password.get().strip()

        if check_credentials(username, password):
            login_window.destroy()  # Close the login window
            open_admin_window()  # Open admin window
        else:
            messagebox.showerror("Error", "Invalid admin credentials.")

    # Admin login UI
    ttk.Label(login_window, text="Admin Username").pack(pady=5)
    entry_username = ttk.Entry(login_window)
    entry_username.pack(pady=5)
    add_placeholder(entry_username, "admin")

    ttk.Label(login_window, text="Admin Password").pack(pady=5)
    entry_password = ttk.Entry(login_window, show="*")
    entry_password.pack(pady=5)
    add_placeholder(entry_password, "admin")

    button_login = ttk.Button(login_window, text="Login", command=attempt_login)
    button_login.pack(pady=10)


# Admin window for managing users and searching student access logs
def open_admin_window():
    admin_window = tk.Toplevel()
    admin_window.title("Admin Panel")
    admin_window.geometry("800x600")

    apply_styles()

    # User table display
    user_table = ttk.Treeview(admin_window, columns=("ID", "First Name", "Last Name", "Status"), show="headings")
    user_table.heading("ID", text="ID")
    user_table.heading("First Name", text="First Name")
    user_table.heading("Last Name", text="Last Name")
    user_table.heading("Status", text="Status")
    user_table.pack(fill=tk.BOTH, expand=True)

    # History table to display sign-in/out records
    history_table = ttk.Treeview(admin_window, columns=("Student ID", "Sign In Time", "Sign Out Time"), show="headings")
    history_table.heading("Student ID", text="Student ID")
    history_table.heading("Sign In Time", text="Sign In Time")
    history_table.heading("Sign Out Time", text="Sign Out Time")
    history_table.pack(fill=tk.BOTH, expand=True, pady=10)

    def refresh_user_table(users=None):
        """Refresh the user table with the provided users, or all users if none are provided."""
        for row in user_table.get_children():
            user_table.delete(row)
        if users is None:
            users = get_users()
        for user in users:
            user_table.insert('', 'end', values=user)

    def refresh_history_table(records):
        """Refresh the history table with search results."""
        for row in history_table.get_children():
            history_table.delete(row)
        for record in records:
            history_table.insert('', 'end', values=record)

    def search_logs():
        """Search for student logs using Student ID or by date range."""
        student_id = student_id_entry.get().strip()
        start_date = start_date_entry.get().strip()
        end_date = end_date_entry.get().strip()

        if student_id:
            # Search by student ID
            if not student_id.isdigit() or len(student_id) != 9:
                messagebox.showerror("Error", "Student ID must be exactly 9 digits.")
                return
            student_logs = get_access_logs_for_student(student_id)
            if student_logs:
                refresh_history_table(student_logs)
            else:
                messagebox.showinfo("No Records", "No access logs found for the entered student ID.")
        elif start_date and end_date:
            # Search by date range
            try:
                logs_by_date = search_by_date_range(start_date, end_date)
                if logs_by_date:
                    refresh_history_table(logs_by_date)
                else:
                    messagebox.showinfo("No Records", "No logs found for the specified date range.")
            except ValueError:
                messagebox.showerror("Error", "Invalid date format. Use YYYY-MM-DD.")
        else:
            messagebox.showerror("Input Error", "Please provide a valid Student ID or a valid date range.")

    # UI for searching by student ID or date range
    search_frame = tk.Frame(admin_window)
    search_frame.pack(pady=10)

    # Search by Student ID
    ttk.Label(search_frame, text="Search by Student ID:").grid(row=0, column=0, padx=10)
    student_id_entry = ttk.Entry(search_frame)
    student_id_entry.grid(row=0, column=1)

    # Search by Date Range
    ttk.Label(search_frame, text="Start Date (YYYY-MM-DD):").grid(row=1, column=0, padx=10)
    start_date_entry = ttk.Entry(search_frame)
    start_date_entry.grid(row=1, column=1)

    ttk.Label(search_frame, text="End Date (YYYY-MM-DD):").grid(row=1, column=2, padx=10)
    end_date_entry = ttk.Entry(search_frame)
    end_date_entry.grid(row=1, column=3)

    # Search button
    search_button = ttk.Button(search_frame, text="Search Logs", command=search_logs)
    search_button.grid(row=2, column=1, pady=10)

    refresh_user_table()

    # UI for toggling student status (activate/suspend)
    def toggle_status():
        student_id = entry_student_id.get().strip()
        if not student_id.isdigit() or len(student_id) != 9:
            messagebox.showerror("Error", "Student ID must be exactly 9 digits.")
            return

        # Check if the student exists
        student_exists = False
        for user in user_table.get_children():
            values = user_table.item(user, 'values')
            if values[0] == student_id:
                student_exists = True
                current_status = values[3]
                new_status = 'active' if current_status == 'suspended' else 'suspended'
                update_user_status(student_id, new_status)
                refresh_user_table()
                messagebox.showinfo("Success", f"User {student_id} status changed to {new_status}.")
                break

        # If student doesn't exist, show popup to add them
        if not student_exists:
            add_student_popup(student_id)

    # UI for student ID input and buttons
    ttk.Label(admin_window, text="Enter Student ID").pack(pady=5)
    entry_student_id = ttk.Entry(admin_window)
    entry_student_id.pack(pady=5)

    button_toggle = ttk.Button(admin_window, text="Activate/Suspend User", command=toggle_status)
    button_toggle.pack(pady=10)

    refresh_user_table()

# Main entry point
if __name__ == "__main__":
    open_regular_window()
