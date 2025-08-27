import tkinter as tk
from tkinter import ttk
from tkinter import messagebox


class LoginPage:
    def __init__(self, parent, admin_manager, customer_manager):
        self.parent = parent
        self.admin_manager = admin_manager
        self.customer_manager = customer_manager

        self.label1 = tk.Label(self.parent, text="Welcome to Movie Store", font=("Bold", 18), background="blue")

        self.label2 = tk.Label(self.parent, text="Login to Movie Store", font=("Bold", 14))
        self.username_entry = ttk.Entry(self.parent)
        self.password_entry = ttk.Entry(self.parent)
        self.login_button = ttk.Button(self.parent, text="Login", command=self.login)

        self.login_callback = None

    def init_components(self):
        self.label1.pack(padx=10, pady=10)
        self.label2.pack(padx=10, pady=10)
        self.username_entry.insert(0, "admin")
        self.password_entry.insert(0, "admin")
        self.username_entry.pack()
        self.password_entry.pack()
        self.login_button.pack()

    def destroy_components(self):
        self.label1.destroy()
        self.label2.destroy()
        self.username_entry.destroy()
        self.password_entry.destroy()
        self.login_button.destroy()

    def set_login_callback(self, callback):
        """Set the callback function to be called on successful login"""
        self.login_callback = callback


    def get_credentials(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        return username, password

    def login(self):
        username, password = self.get_credentials()
        isAdmin, admin_name = self.admin_manager.authenticate_admin(username, password)
        if isAdmin:
            # messagebox.showinfo("Success", f"Welcome Admin {admin_name}")
            if self.login_callback:
                self.login_callback()
        else:
            messagebox.showinfo("Failed", "Invalid credentials")
