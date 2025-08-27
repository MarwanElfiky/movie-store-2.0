import tkinter as tk
from tkinter import ttk
from register_customer_tab import CustomerAddingTab
from login_page import LoginPage
from add_movie_tab import AddMovieTab
from movies_status_tab import MoviesStatusTab
from customer_status_tab import CustomerStatus
from data_manager import CustomerManager, AdminManager, MovieManager, RentalManager


# Dependency Injection Container #f8f9fa #2e2c2c
class Main:
    def __init__(self, master):
        self.login_page = None
        self.master = master
        self.master.title("Movie Store Prototype")
        self.master.state('zoomed')
        self.master.configure(bg="#2e2c2c")

        self.admin_manager = AdminManager()
        self.customer_manager = CustomerManager()
        self.movie_manager = MovieManager()
        self.rental_manager = RentalManager(self.customer_manager, self.movie_manager)

        self.show_login_page()

    def show_login_page(self):
        self.login_page = LoginPage(self.master, self.admin_manager, self.customer_manager)
        self.login_page.init_components()
        self.login_page.set_login_callback(self.on_login_success)

    def on_login_success(self):
        """Called when login is successful"""
        self.login_page.destroy_components()
        self.create_main_interface()


    def create_main_interface(self):
        style = ttk.Style()
        style.configure('TNotebook', background='#2e2c2c', borderwidth=0)
        style.configure('TFrame', background='#2e2c2c', borderwidth=0)

        main_notebook = ttk.Notebook(self.master)
        employee_tab = ttk.Frame(main_notebook)
        admin_tab = ttk.Frame(main_notebook)

        employee_frame_notebook = ttk.Notebook(employee_tab)
        admin_frame_notebook = ttk.Notebook(admin_tab)

        creating_customer_tab_frame = ttk.Frame(employee_frame_notebook)
        customer_status_tab_frame = ttk.Frame(employee_frame_notebook)

        adding_movie_tab_frame = ttk.Frame(admin_frame_notebook)
        movies_status_tab_frame = ttk.Frame(admin_frame_notebook)

        # Dependency Injections
        register_customer_tab = CustomerAddingTab(creating_customer_tab_frame, self.customer_manager, self.movie_manager, self.rental_manager)

        add_movie_tab = AddMovieTab(adding_movie_tab_frame, self.movie_manager, register_customer_tab.refresh_movie_dropdown)

        movies_status_tab = MoviesStatusTab(movies_status_tab_frame, self.movie_manager)

        customers_status_tab = CustomerStatus(customer_status_tab_frame, self.customer_manager, self.rental_manager, register_customer_tab.refresh_customer_dropdown)

        register_customer_tab.init_components()
        register_customer_tab.update_textboxes()

        employee_tab.pack(fill=tk.BOTH, expand=True)
        admin_tab.pack(fill=tk.BOTH, expand=True)
        creating_customer_tab_frame.pack(fill=tk.BOTH, expand=True)
        adding_movie_tab_frame.pack(fill=tk.BOTH, expand=True)

        add_movie_tab.init_components()
        add_movie_tab.update_textboxes()

        movies_status_tab.init_components()
        customers_status_tab.init_components()

        main_notebook.add(employee_tab, text="Employee Tab")
        main_notebook.add(admin_tab, text="Admin Tab", state="normal")

        employee_frame_notebook.add(creating_customer_tab_frame, text="Register Customer")
        employee_frame_notebook.add(customer_status_tab_frame, text="Customer Status")

        admin_frame_notebook.add(adding_movie_tab_frame, text="Add a movie")
        admin_frame_notebook.add(movies_status_tab_frame, text="Movie Status")

        main_notebook.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)

        employee_frame_notebook.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)
        admin_frame_notebook.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)




if __name__ == "__main__":
    root = tk.Tk()
    window = Main(root)
    root.mainloop()
