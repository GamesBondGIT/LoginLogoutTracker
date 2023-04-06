import os
import sys
import time
import datetime
import tkinter as tk
from tkinter import messagebox
import pyautogui
import psutil
from datetime import timedelta
from PIL import ImageTk, Image

# Define the path to the credentials file
CREDENTIALS_FILE = r"C:\Users\Public\Documents\Security\credentials.txt"

# Define the path to the log file directory
LOG_FILE_DIR = r"C:\Users\Public\Documents\Security"

# Define the maximum number of login attempts
MAX_LOGIN_ATTEMPTS = 3

# Define the shutdown delay in seconds
SHUTDOWN_DELAY = 20


class LoginLogoutTracker:
    def __init__(self):
        self.username = None
        self.password = None
        self.login_attempts = 0
        self.is_logged_in = False
        self.is_logging_out = False
        self.log_data = ""

        # Initialize the GUI
        self.init_gui()

    def init_gui(self):
        # Create the main window
        self.root = tk.Tk()
        self.root.title("LOGIN LOGOUT TRACKER")
        self.root.attributes("-topmost", True)

        # Set full screen mode
        self.root.attributes('-fullscreen', True)

        # Remove Close Functionality
        self.root.protocol("WM_DELETE_WINDOW", lambda: None)

        # Create the login frame
        self.login_frame = tk.Frame(self.root)
        self.login_frame.pack(fill=tk.BOTH, expand=True)

        # Create the login form
        self.login_username_label = tk.Label(self.login_frame, text="Username:")
        self.login_username_label.pack(side=tk.LEFT, padx=10, pady=10)
        self.login_username_entry = tk.Entry(self.login_frame)
        self.login_username_entry.pack(side=tk.LEFT, padx=10, pady=10)
        self.login_password_label = tk.Label(self.login_frame, text="Password:")
        self.login_password_label.pack(side=tk.LEFT, padx=10, pady=10)
        self.login_password_entry = tk.Entry(self.login_frame, show="*")
        self.login_password_entry.pack(side=tk.LEFT, padx=10, pady=10)
        self.login_button = tk.Button(self.login_frame, text="LOGIN", command=self.login)
        self.login_button.pack(side=tk.LEFT, padx=10, pady=10)

        # Create the logout frame
        self.logout_frame = tk.Frame(self.root)
        self.logout_frame.pack(fill=tk.BOTH, expand=True)

        # Create the logout form
        self.logout_username_label = tk.Label(self.logout_frame, text="Username:")
        self.logout_username_label.pack(side=tk.LEFT, padx=10, pady=10)
        self.logout_username_entry = tk.Entry(self.logout_frame)
        self.logout_username_entry.pack(side=tk.LEFT, padx=10, pady=10)
        self.logout_password_label = tk.Label(self.logout_frame, text="Password:")
        self.logout_password_label.pack(side=tk.LEFT, padx=10, pady=10)
        self.logout_password_entry = tk.Entry(self.logout_frame, show="*")
        self.logout_password_entry.pack(side=tk.LEFT, padx=10, pady=10)
        self.logout_logdata_label = tk.Label(self.logout_frame, text="Log data:")
        self.logout_logdata_label.pack(side=tk.LEFT, padx=10, pady=10)
        self.logout_logdata_entry = tk.Entry(self.logout_frame)
        self.logout_logdata_entry.pack(side=tk.LEFT, padx=10, pady=10)
        self.logout_button = tk.Button(self.logout_frame, text="LOGOUT", command=self.logout)
        self.logout_button.pack(side=tk.LEFT, padx=10, pady=10)


        # Hide the logout frame initially
        self.hide_logout_frame()

        # Start the GUI main loop
        self.root.mainloop()

    def login(self):
        # Get the username and password from the form
        self.username = self.login_username_entry.get().strip()
        self.password = self.login_password_entry.get().strip()

        # Check the credentials
        if self.check_credentials(self.username, self.password):
            # Show a success message and hide the login frame
            messagebox.showinfo("Success", "Welcome, have a great day!")
            self.hide_login_frame()

            # Start the activity tracking loop
            self.start_activity_tracking()
        else:
            # Increment the login attempts
            self.login_attempts += 1

            if self.login_attempts < MAX_LOGIN_ATTEMPTS:
                # Show a warning message with the remaining attempts
                messagebox.showwarning("Warning", f"Wrong username and password, {MAX_LOGIN_ATTEMPTS - self.login_attempts} more tries left.")
            else:
                # Show a warning message and shutdown the system after a delay
                messagebox.showwarning("Warning", "Wrong username and password, system will shutdown in 20 seconds.")
                self.shutdown_system()

    def logout(self):
        # Get the username and password from the form
        username = self.logout_username_entry.get().strip()
        password = self.logout_password_entry.get().strip()
        logdata = self.logout_logdata_entry.get().strip()

        # Check the credentials and log data
        if not username or not password or not logdata:
            # Show a warning message
            messagebox.showwarning("Warning", "Wrong username and password (or) empty log data.")
            return

        if not self.check_credentials(username, password):
            # Show a warning message
            messagebox.showwarning("Warning", "Wrong username and password (or) empty log data.")
            return

        # Set the log data
        self.log_data = logdata

        # Set the logging out flag
        self.is_logging_out = True

    def start_activity_tracking(self):
        while True:
            # Check if the user is idle
            if pyautogui.isIdle():
                # Log the idle time
                self.log_activity("IDLE")

            # Sleep for 1 second
            time.sleep(1)

            # Check if the user is logging out / shutting down
            if self.is_logging_out:
                # Log the logout time and data
                self.log_activity("LOGOUT")
                self.save_log_file()

                # Show a message and hide the logout frame
                messagebox.showinfo("Success", "System will shutdown in 20 seconds.")
                self.hide_logout_frame()

                # Shutdown the system after a delay
                self.shutdown_system()

    def log_activity(self, activity):
        # Get the current timestamp
        now = datetime.datetime.now()
        timestamp = now.strftime("%H:%M - %d/%m/%y")

        # Format the activity and timestamp
        log_line = f"{activity} - {timestamp}\n"

        # Append the log line to the log data
        self.log_data += log_line

    def save_log_file(self):
        # Get the current date and username
        now = datetime.datetime.now()
        date_str = now.strftime("%d-%m-%Y")
        username_str = self.username.replace(" ", "_")

        # Construct the log file name
        log_file_name = f"{date_str}-{username_str}.txt"

        # Construct the log file path
        log_file_path = os.path.join(LOG_FILE_DIR, log_file_name)

        # Save the log data to the log file
        with open(log_file_path, "a") as f:
            f.write(f"TODAY'S LOG:\n{self.log_data}\n")

    def check_credentials(self, username, password):
        # Read the credentials from the credentials file
        with open(CREDENTIALS_FILE, "r") as f:
            credentials = f.read()

        # Split the credentials into username and password pairs
        credentials = [tuple(line.strip().split(":")) for line in credentials.split("\n")]

        # Check if the username and password are valid
        return any((u == username and p == password) for u, p in credentials)

    def get_active_window_title(self):
        # Get the window handle of the active window
        hwnd = pyautogui.getActiveWindow().hwnd

        # Get the window title
        title = psutil.Process(hwnd).name()

        return title

    def hide_login_frame(self):
        # Hide the login frame and show the logout frame
        self.login_frame.pack_forget()
        self.show_logout_frame()

    def show_logout_frame(self):
        # Show the logout frame and focus on the logout username entry
        self.logout_frame.pack(fill=tk.BOTH, expand=True)
        self.logout_username_entry.focus_set()

    def hide_logout_frame(self):
        # Hide the logout frame and show the login frame
        self.logout_frame.pack_forget()
        self.login_frame.pack(fill=tk.BOTH, expand=True)

    def shutdown_system(self):
        # Wait for the delay
        time.sleep(SHUTDOWN_DELAY)

        # Shutdown the system
        os.system("shutdown /s /t 0")

if __name__ == "__main__":
    app = LoginLogoutTracker()
