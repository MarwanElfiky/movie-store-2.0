import tkinter as tk
from tkinter import ttk, messagebox


class AddMovieTab:
    def __init__(self, frame, movie_manager, movie_added_callback=None):
        self.frame = frame
        self.movie_manager = movie_manager

        self.add_movie_wrapper = tk.LabelFrame(self.frame, text="Add Movie", background="#2e2c2c", foreground="white")

        self.movie_name_entry = ttk.Entry(self.add_movie_wrapper)
        self.movie_copies_count = ttk.Entry(self.add_movie_wrapper)
        self.movie_daily_fees = ttk.Entry(self.add_movie_wrapper)
        self.daily_overdue_fee = ttk.Entry(self.add_movie_wrapper)
        self.max_rental_days = ttk.Entry(self.add_movie_wrapper)

        self.movie_added_callback = movie_added_callback

    def init_components(self):
        self.add_movie_wrapper.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        tk.Label(self.add_movie_wrapper, text="Enter Movie Title :", background="#2e2c2c", foreground="white").pack()
        self.movie_name_entry.pack()
        tk.Label(self.add_movie_wrapper, text="Enter Number of copies :", background="#2e2c2c", foreground="white").pack()
        self.movie_copies_count.pack()
        tk.Label(self.add_movie_wrapper, text="Enter Rental fees (per day) :", background="#2e2c2c", foreground="white").pack()
        self.movie_daily_fees.pack()
        tk.Label(self.add_movie_wrapper, text="Enter daily overdue fee :", background="#2e2c2c", foreground="white").pack()
        self.daily_overdue_fee.pack()
        tk.Label(self.add_movie_wrapper, text="Enter maximum rental days :", background="#2e2c2c", foreground="white").pack()
        self.max_rental_days.pack()
        ttk.Button(self.add_movie_wrapper, text="Save Movie", command=self.save_movie).pack()

    def validate_movie_name(self):
        if not self.movie_name_entry.get():
            messagebox.showwarning("Warning", "Invalid input")
            return False
        return True

    def validate_movie_copies_count(self):
        if not self.movie_copies_count.get():
            messagebox.showwarning("Warning", "Invalid input")
            return False
        return True

    def validate_movie_rental_fees(self):
        if not self.movie_daily_fees.get():
            messagebox.showwarning("Warning", "Invalid input")
            return False
        return True

    def validate_daily_overdue_fee(self):
        if not self.daily_overdue_fee.get():
            messagebox.showwarning("Warning", "Invalid input")
            return False
        return True

    def validate_max_rental_days(self):
        if not self.max_rental_days.get():
            messagebox.showwarning("Warning", "Invalid input")
            return False
        return True

    def save_movie(self):
        if not self.validate_movie_name():
            return
        if not self.validate_movie_copies_count():
            return
        if not self.validate_movie_rental_fees():
            return
        if not self.validate_daily_overdue_fee():
            return
        if not self.validate_max_rental_days():
            return

        movie_name = self.movie_name_entry.get()
        movie_copies_count = int(self.movie_copies_count.get())
        movie_rental_fee = float(self.movie_daily_fees.get())
        movie_daily_overdue = float(self.daily_overdue_fee.get())
        movie_max_rental_days = int(self.max_rental_days.get())

        if messagebox.askyesno(title="Confirm Register", message="Are you sure you want to Register ?"):
            movie_created, movies_count = self.movie_manager.save_to_database(movie_name, movie_copies_count, movie_rental_fee, movie_daily_overdue, movie_max_rental_days)
            if movie_created:
                messagebox.showinfo("Success", f"Movie successfully added\nTotal Movies : {movies_count}")

                # "Make the phone call" if we have a number
                if self.movie_added_callback:
                    self.movie_added_callback()  # Call the employee's function

                self.movie_name_entry.delete(0, tk.END)
                self.movie_copies_count.delete(0, tk.END)
                self.movie_daily_fees.delete(0, tk.END)
                self.daily_overdue_fee.delete(0, tk.END)
                self.max_rental_days.delete(0, tk.END)

    def update_textboxes(self):
        self.movie_name_entry.delete(0, tk.END)
        self.movie_name_entry.insert(0, "Marvel")
        self.movie_copies_count.delete(0, tk.END)
        self.movie_copies_count.insert(0, "3")
        self.movie_daily_fees.delete(0, tk.END)
        self.movie_daily_fees.insert(0, "0.5")
        self.daily_overdue_fee.delete(0, tk.END)
        self.daily_overdue_fee.insert(0, "2")
        self.max_rental_days.delete(0, tk.END)
        self.max_rental_days.insert(0, "3")
