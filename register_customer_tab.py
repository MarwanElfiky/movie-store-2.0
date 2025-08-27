import tkinter as tk
from tkinter import ttk
from tkinter import messagebox


class CustomerAddingTab:
    def __init__(self, frame, customer_manager, movie_manager, rental_manager):
        self.frame = frame
        self.customer_manager = customer_manager
        self.movie_manager = movie_manager
        self.rental_manager = rental_manager

        # Wrapper 1 initializations
        self.register_customer_wrapper = tk.LabelFrame(self.frame, text="Register Customer", font=("arial", 12),
                                                       background="#2e2c2c", foreground="white")
        # Wrapper 1 Textboxes
        self.customer_name = ttk.Entry(self.register_customer_wrapper)
        self.customer_username = ttk.Entry(self.register_customer_wrapper)
        self.customer_phone_number = ttk.Entry(self.register_customer_wrapper)

        # Wrapper 2 initializations
        self.rent_movie_to_customer_wrapper = tk.LabelFrame(self.frame, text="Rent Movie", font=("arial", 12),
                                                            background="#2e2c2c", foreground="white")
        # Wrapper 2 frames
        self.top_controls_frame = tk.Frame(self.rent_movie_to_customer_wrapper, background="#2e2c2c")
        self.bottom_controls_frame = tk.Frame(self.rent_movie_to_customer_wrapper, background="#2e2c2c")

        # Wrapper 2 Widgets :

        # Customers Dropbox
        available_customers = self.get_customers()
        self.customer_dropbox = ttk.Combobox(self.top_controls_frame,
                                             values=available_customers, width=30, state="readonly")
        self.customer_dropbox.set("Select a Customer")

        # Movies Dropbox
        available_movies = self.get_movies()
        self.movies_dropbox = ttk.Combobox(self.top_controls_frame, values=available_movies, width=30, state="readonly")
        self.movies_dropbox.set("Select a Movie")

        # Treeviews :

        # Movie Treeview
        self.movie_tree_columns = ["Movie Name", "Copies Available", "Daily fee", "Daily Overdue Fee",
                                   "Max Rental Days"]
        self.movie_tree = ttk.Treeview(self.rent_movie_to_customer_wrapper, columns=self.movie_tree_columns, height=1,
                                       show="headings")
        for column in self.movie_tree_columns:
            self.movie_tree.heading(column, text=str(column.strip()))
            self.movie_tree.column(column, width=100)

        # Customer Treeview
        self.customer_tree_columns = ["Rented Movies", "Rented On", "Returned On", "Due Date", "Overdue"]
        self.customer_tree = ttk.Treeview(self.rent_movie_to_customer_wrapper, columns=self.customer_tree_columns,
                                          height=4, show="headings")
        for column in self.customer_tree_columns:
            self.customer_tree.heading(column, text=str(column.strip()))
            self.customer_tree.column(column, width=100)

        self.rented_days_entry = ttk.Entry(self.bottom_controls_frame)

        # Wrapper 3 widgets:
        self.wrapper3_frame = tk.LabelFrame(self.frame, text="Return Movie", font=("arial", 12),
                                            background="#2e2c2c", foreground="white")

    def init_components(self):

        # Wrapper 1 Components :

        self.register_customer_wrapper.pack(fill=tk.X, side='top', anchor='nw', padx=30, pady=30)
        ttk.Label(self.register_customer_wrapper, text="Customer Name :", font=("arial", 10), background="#2e2c2c",
                  foreground="white").pack(side='left', anchor='nw', padx=20, pady=10)
        self.customer_name.pack(side='left', anchor='nw', padx=20, pady=10)
        ttk.Label(self.register_customer_wrapper, text="Customer Username :", font=("arial", 10), background="#2e2c2c",
                  foreground="white").pack(side='left', anchor='nw', padx=20, pady=10)
        self.customer_username.pack(side='left', anchor='nw', padx=20, pady=10)
        ttk.Label(self.register_customer_wrapper, text="Phone Number :", font=("arial", 10), background="#2e2c2c",
                  foreground="white").pack(side='left', anchor='nw', padx=20, pady=10)
        self.customer_phone_number.pack(side='left', anchor='nw', padx=20, pady=10)
        ttk.Button(self.register_customer_wrapper, text="Save Customer", command=self.save_customer).pack(side='left',
                                                                                                          anchor='ne',
                                                                                                          padx=50,
                                                                                                          pady=5)
        ttk.Button(self.register_customer_wrapper, text="Clear Input", command=self.clear_input).pack(side='left',
                                                                                                      anchor='ne',
                                                                                                      padx=50, pady=5)
        # Wrapper 2 Components:

        self.rent_movie_to_customer_wrapper.pack(fill=tk.BOTH, side='top', anchor='nw', padx=30, pady=30)

        # Create top controls frame
        self.top_controls_frame.pack(side='top', fill='x', pady=5, padx=10)

        ttk.Label(self.top_controls_frame, text="Available Customers :", font=("arial", 10),
                  background="#2e2c2c", foreground="white").pack(side='left', anchor='nw', padx=20, pady=10)
        self.customer_dropbox.pack(side='left', anchor='nw', padx=20, pady=10)

        ttk.Label(self.top_controls_frame, text="Available Movies :", font=("arial", 10),
                  background="#2e2c2c", foreground="white").pack(side='left', anchor='nw', padx=20, pady=10)
        self.movies_dropbox.pack(side='left', anchor='nw', padx=20, pady=10)

        ttk.Button(self.top_controls_frame, text="Load", command=self.fill_trees).pack(side='left', anchor='ne',
                                                                                       padx=50,
                                                                                       pady=5)

        # Pack TreeViews below controls
        self.movie_tree.pack(side='top', anchor='w', expand=True, fill='both', padx=20, pady=10)
        self.customer_tree.pack(side='top', anchor='w', expand=True, fill='both', padx=20, pady=10)

        # Create bottom controls frame
        self.bottom_controls_frame.pack(side='bottom', fill='x', pady=5)

        ttk.Label(self.bottom_controls_frame, text="How many days to rent :", font=("arial", 10),
                  background="#2e2c2c", foreground="white").pack(side='top', anchor='w', padx=20, pady=5)
        self.rented_days_entry.pack(side='top', anchor='w', padx=20, pady=5)

        ttk.Button(self.bottom_controls_frame, text="Rent", command=self.rent).pack(side='left', anchor='w', padx=20,
                                                                                    pady=5)

        # Wrapper 3 init:
        self.wrapper3_frame.pack(fill=tk.BOTH, side='top', anchor='nw', padx=30, pady=30)
        ttk.Button(self.wrapper3_frame, text="show", command=self.load_customers_with_rentals).pack(side='left',
                                                                                                    anchor='w', padx=20,
                                                                                                    pady=5)

    def validate_name(self):
        if not self.customer_name.get():
            self.customer_name.focus_set()
            messagebox.showwarning(title="Warning", message="Name can't be empty")
            return False
        return True

    def validate_username(self):
        if not self.customer_username.get():
            self.customer_username.focus_set()
            messagebox.showwarning(title="Warning", message="invalid username input")
            return False

        return True

    def validate_phone(self):
        phone = self.customer_phone_number.get()

        if not self.customer_phone_number.get():
            self.customer_phone_number.focus_set()
            messagebox.showwarning(title="Warning", message="invalid phone input")
            return False

        if len(phone) != 11:
            self.customer_phone_number.focus_set()
            messagebox.showwarning(title="Warning", message="phone must contains 11 digits")
            return False

        if type(int(self.customer_phone_number.get())) is not type(int()):
            self.customer_phone_number.focus_set()
            messagebox.showwarning(title="Warning", message="phone can only be a number")
            return False

        return True

    def save_customer(self):
        if not self.validate_name():
            return
        if not self.validate_username():
            return
        if not self.validate_phone():
            return

        if messagebox.askyesno(title="Confirm Register", message="Are you sure you want to Register ?"):
            customer_name = self.customer_name.get()
            customer_username = self.customer_username.get()
            customer_phone = self.customer_phone_number.get()
            customer_created, customer_count = self.customer_manager.save_customer_to_system(customer_name,
                                                                                             customer_username,
                                                                                             customer_phone)
            if customer_created:
                self.customer_name.delete(0, tk.END)
                self.customer_username.delete(0, tk.END)
                self.customer_phone_number.delete(0, tk.END)
                updated_customers = self.get_customers()
                self.customer_dropbox['values'] = updated_customers
                messagebox.showinfo("Success", f"Customer successfully added\nTotal customers : {customer_count}")
                self.customer_name.focus_set()

    def update_textboxes(self):
        self.customer_name.delete(0, tk.END)
        self.customer_name.insert(0, "Hamza")
        self.customer_username.delete(0, tk.END)
        self.customer_username.insert(0, "Hamzawy")
        self.customer_phone_number.delete(0, tk.END)
        self.customer_phone_number.insert(0, "01068036406")

    def clear_input(self):
        self.customer_name.delete(0, tk.END)
        self.customer_username.delete(0, tk.END)
        self.customer_phone_number.delete(0, tk.END)

    def get_customers(self):
        customers = self.customer_manager.retrieve_customers_from_database()
        customers_list = []
        for customer_username, customer in customers.items():
            customers_list.append(customer.name)
        return customers_list

    def get_movies(self):
        available_movies = self.movie_manager.retrieve_movies_from_database()
        movie_list = []
        if available_movies:
            for movie_name, movie in available_movies.items():
                movie_list.append(movie.name)
            return movie_list

    def refresh_movie_dropdown(self):
        """This is the 'phone number' - the function that gets called"""
        self.movies_dropbox.set("Select a movie")
        updated_movies = self.get_movies()  # Get fresh movie list
        self.movies_dropbox['values'] = updated_movies  # Update dropdown

    def refresh_customer_dropdown(self):
        self.customer_dropbox.set("Select a customer")
        updated_customer = self.get_customers()
        self.customer_dropbox['values'] = updated_customer

    def fill_trees(self):
        selected_movie = self.movies_dropbox.get()
        selected_customer = self.customer_dropbox.get()

        available_movies = self.movie_manager.retrieve_movies_from_database()
        available_customers = self.customer_manager.retrieve_customers_from_database()

        if available_movies:
            for movie_name, movie in available_movies.items():
                if movie_name == selected_movie:
                    self.clear_movie_tree()
                    self.movie_tree.insert('', tk.END, values=[movie.name, movie.available_for_rent(), movie.daily_fee,
                                                               movie.daily_overdue_fees, movie.max_rental_days])

        customer, error = self.customer_manager.get_customer_by_name(selected_customer)

        if error:
            return

        active_rentals = self.rental_manager.get_customer_active_rental_by_id(customer.id)

        if available_customers:
            self.clear_customer_tree()
            for rental in active_rentals:
                rental_id = rental['rental_id']

                # Get real overdue status
                if rental_id in self.rental_manager.active_transactions:
                    transaction = self.rental_manager.active_transactions[rental_id]
                    is_overdue = transaction.is_overdue()
                    overdue_text = "Yes" if is_overdue else "No"

                    if is_overdue:
                        days_late = transaction.days_late()
                        overdue_text = f"Yes ({days_late} days)"
                else:
                    overdue_text = "Unknown"

                self.customer_tree.insert('', tk.END, values=[
                    rental['movie_name'],
                    rental['rental_date'],
                    '',  # returned_on (empty for active rentals)
                    rental['due_date'],
                    overdue_text  # Real overdue status instead of hardcoded "No"
                ])

    def clear_movie_tree(self):
        for items in self.movie_tree.get_children():
            self.movie_tree.delete(items)

    def clear_customer_tree(self):
        for items in self.customer_tree.get_children():
            self.customer_tree.delete(items)

    def rent(self):
        movie_name = self.movies_dropbox.get()
        customer_name = self.customer_dropbox.get()
        days_to_rent = int(self.rented_days_entry.get())

        if movie_name == "Choose a Movie":
            messagebox.showerror("Error", "Please select a movie")
            return

        if customer_name == "Choose a Customer":
            messagebox.showerror("Error", "Please select a customer")
            return

        success, error = self.rental_manager.rent_movie(movie_name, customer_name, days_to_rent)

        if error:
            messagebox.showerror("Rental Failed", error)
        else:
            if messagebox.askyesno(title="Confirm Rental", message="Are you sure you want to rent"):
                messagebox.showinfo("Success", "Movie rented successfully")
                self.fill_trees()
                self.rented_days_entry.delete(0, tk.END)

    def load_customers_with_rentals(self):
        selected_customer = self.customer_dropbox.get()
        customer, error = self.customer_manager.get_customer_by_name(selected_customer)
        if error:
            print(error)
            return
        active_rentals = self.rental_manager.get_customer_active_rental_by_id(customer.id)
        print(active_rentals)
