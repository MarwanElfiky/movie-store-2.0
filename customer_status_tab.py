from tkinter import ttk, messagebox
import tkinter as tk


class CustomerStatus:
    def __init__(self, frame, customer_manager, rental_manager, customer_deleted_callback=None):

        self.customer_deleted_callback = customer_deleted_callback

        self.frame = frame
        self.customer_manager = customer_manager
        self.rental_manager = rental_manager

        self.customer_list_wrapper = tk.LabelFrame(self.frame, text="Customer List", background="#2e2c2c", foreground="white")
        self.search_customer_wrapper = tk.LabelFrame(self.frame, text="Search Customer", background="#2e2c2c", foreground="white")
        self.customer_data_wrapper = tk.LabelFrame(self.frame, text="Customer Data", background="#2e2c2c", foreground="white")

        self.customers_tree = ttk.Treeview(self.customer_list_wrapper, columns=['username', 'phone', 'status'], height=6)
        self.movies_tree = ttk.Treeview(self.customer_list_wrapper, columns=['rented_on', 'returned_on', 'due_date', 'is_overdue'], height=6)

        self.customers_tree.heading("#0", text="Customer Name")
        self.customers_tree.heading("username", text="Username")
        self.customers_tree.heading("phone", text="Phone")
        self.customers_tree.heading("status", text="Status")

        self.customers_tree.column("#0", width=100)
        self.customers_tree.column("username", width=100)
        self.customers_tree.column("phone", width=80)
        self.customers_tree.column("status", width=50)

        self.movies_tree.heading("#0", text="Rented Movies")
        self.movies_tree.heading("rented_on", text="Rented On")
        self.movies_tree.heading("returned_on", text="Returned On")
        self.movies_tree.heading("due_date", text="Due Date")
        self.movies_tree.heading("is_overdue", text="Overdue")

        self.movies_tree.column("#0", width=100)
        self.movies_tree.column("rented_on", width=100)
        self.movies_tree.column("returned_on", width=100)
        self.movies_tree.column("due_date", width=100)
        self.movies_tree.column("is_overdue", width=100)



        self.customers_tree.bind('<Double-Button-1>', self.get_from_treeview)
        self.customers_tree.bind('<ButtonRelease-1>', self.insert_into_treeview2)

        self.separator = ttk.Separator(self.customer_list_wrapper, orient=tk.VERTICAL)

        self.search_textbox = ttk.Entry(self.search_customer_wrapper)

        self.customer_name_update_textbox = ttk.Entry(self.customer_data_wrapper)
        self.customer_username_update_textbox = ttk.Entry(self.customer_data_wrapper)

    def init_components(self):
        # Initialize Containers
        self.customer_list_wrapper.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        self.search_customer_wrapper.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        self.customer_data_wrapper.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Treeview Container
        tk.Label(self.customer_list_wrapper, text="Load Customers :", background="#2e2c2c", foreground="white").pack(side=tk.LEFT, padx=10)
        ttk.Button(self.customer_list_wrapper, text="Load Customers", command=self.load_customers_to_tree).pack(side=tk.LEFT, padx=10)
        ttk.Button(self.customer_list_wrapper, text="Clear", command=self.clear_tree).pack(side=tk.LEFT, padx=10)
        self.customers_tree.pack(side=tk.LEFT, padx=10)
        self.separator.pack(side=tk.LEFT, fill=tk.Y, padx=10)
        self.movies_tree.pack(side=tk.LEFT, padx=10)

        # Search Container
        tk.Label(self.search_customer_wrapper, text="Search", background="#2e2c2c", foreground="white").pack(side=tk.LEFT, padx=10)
        self.search_textbox.pack(side=tk.LEFT, padx=10)
        ttk.Button(self.search_customer_wrapper, text="Search", command=self.search_customer).pack(side=tk.LEFT, padx=10)
        ttk.Button(self.search_customer_wrapper, text="Clear", command=self.load_customers_to_tree).pack(side=tk.LEFT, padx=10)

        # Update Customer Data Container
        tk.Label(self.customer_data_wrapper, text="Name :", background="#2e2c2c", foreground="white").grid(row=0, column=1, padx=5, pady=3)
        self.customer_name_update_textbox.grid(row=0, column=2, padx=5, pady=3)
        tk.Label(self.customer_data_wrapper, text="Username :", background="#2e2c2c", foreground="white").grid(row=1, column=1, padx=5, pady=3)
        self.customer_username_update_textbox.grid(row=1, column=2, padx=5, pady=5)

        ttk.Button(self.customer_data_wrapper, text="Update", command=self.update_customer_data).grid(row=2, column=1, padx=17, pady=5)
        ttk.Button(self.customer_data_wrapper, text="Delete", command=self.delete_selected_customer).grid(row=2, column=2, padx=17, pady=5)



    def load_customers_to_tree(self):
        self.clear_tree()
        customers = self.customer_manager.retrieve_customers_from_database()
        if customers:
            for customer_username, customer_data in customers.items():
                self.customers_tree.insert("", tk.END, text=customer_data.name,
                                           values=[customer_username, customer_data.phone, customer_data.account_status])

    def clear_tree(self):
        for items in self.customers_tree.get_children():
            self.customers_tree.delete(items)

    def search_customer(self):
        customers = self.customer_manager.retrieve_customers_from_database()
        for customer_username, data in customers.items():
            if self.search_textbox.get() == data.name:
                self.clear_tree()
                self.customers_tree.insert("", tk.END, text=data.name, values=[customer_username, data.phone, data.active_rentals, data.account_status])

    def get_username_from_tree(self):
        item = self.customers_tree.item(self.customers_tree.focus())
        customer_username = item['values'][0]
        return customer_username, item

    # Callback function
    def get_from_treeview(self, event):
        customer_username, item = self.get_username_from_tree()
        customer_name = item['text']

        self.customer_name_update_textbox.delete(0, tk.END)
        self.customer_name_update_textbox.insert(0, customer_name)
        self.customer_username_update_textbox.delete(0, tk.END)
        self.customer_username_update_textbox.insert(0, customer_username)

        return customer_username, customer_name

    def insert_into_treeview2(self, event):
        for item in self.movies_tree.get_children():
            self.movies_tree.delete(item)

            # Get customer
        item = self.customers_tree.item(self.customers_tree.focus())
        if not item['values']:  # No item selected
            return

        customer_name = item['text']  # Customer name is in text

        customer, error = self.customer_manager.get_customer_by_name(customer_name)
        if error:
            print(f"Error getting customer: {error}")
            return

        print(f"Found customer: {customer.name}, ID: {customer.id}")

        # Get customer's active rentals
        active_rentals = self.rental_manager.get_customer_active_rental_by_id(customer.id)
        print(f"Active rentals found: {len(active_rentals)}")

        # Populate tree with real overdue status
        for rental in active_rentals:
            rental_id = rental['rental_id']

            # Get the actual transaction to check overdue status
            if rental_id in self.rental_manager.active_transactions:
                transaction = self.rental_manager.active_transactions[rental_id]
                is_overdue = transaction.is_overdue()
                overdue_text = "Yes" if is_overdue else "No"

                # Add days late info if overdue
                if is_overdue:
                    days_late = transaction.days_late()
                    overdue_text = f"Yes ({days_late} days)"
            else:
                overdue_text = "Unknown"

            self.movies_tree.insert('', tk.END, text=rental['movie_name'], values=[
                rental['rental_date'],
                '',  # returned_on (empty for active rentals)
                rental['due_date'],
                overdue_text  # Real overdue status
            ])

    def update_customer_data(self):
        original_customer_username, item = self.get_username_from_tree()

        new_username = self.customer_username_update_textbox.get()
        new_name = self.customer_name_update_textbox.get()

        if messagebox.askyesno(title="Confirm Update", message="Are you sure you want to update ?"):
            success, message = self.customer_manager.update_customer(original_customer_username, new_name, new_username)

            if success:
                if self.customer_deleted_callback:
                    self.customer_deleted_callback()
                self.load_customers_to_tree()
                print(message)



    def delete_selected_customer(self):
        original_customer_username, item = self.get_username_from_tree()
        print(original_customer_username)
        if messagebox.askyesno(title="Confirm Update/Delete", message="Confirm ?"):
            success, message = self.customer_manager.delete_customer(original_customer_username)

            if success:
                if self.customer_deleted_callback:
                    self.customer_deleted_callback()
                print(message)
                self.load_customers_to_tree()


