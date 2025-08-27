import tkinter as tk
from tkinter import ttk


class MoviesStatusTab:
    def __init__(self, frame, movie_manager):
        self.frame = frame
        self.movie_manager = movie_manager

        self.first_frame = ttk.Frame(self.frame)

        self.columns = ['copy id', 'status']
        self.movies_tree = ttk.Treeview(self.first_frame, columns=self.columns, height=5)
        self.movies_tree.heading("#0", text="Movie name")
        self.movies_tree.heading("copy id", text="Copy id")
        self.movies_tree.heading("status", text="Status")

        self.movies_tree.column("#0", width=100)
        self.movies_tree.column("copy id", width=250)
        self.movies_tree.column("status", width=100)

    def init_components(self):
        self.first_frame.pack(side='top', fill='x', pady=5, padx=10)
        tk.Label(self.first_frame, text="Load Movies :", background="#2e2c2c", foreground="white").pack(side='left', anchor='nw', padx=20, pady=10)
        ttk.Button(self.first_frame, text="Load movies", command=self.load_data_to_tree).pack(side='left', anchor='nw', padx=20, pady=10)
        self.movies_tree.pack(side='left', anchor='nw', padx=20, pady=10)
        tk.Label(self.first_frame, text="Clear :", background="#2e2c2c", foreground="white").pack(side='left', anchor='nw', padx=20, pady=10)
        ttk.Button(self.first_frame, text="Clear", command=self.clear_tree).pack(side='left', anchor='nw', padx=20, pady=10)

    def load_data_to_tree(self):
        self.clear_tree()
        data_retrieved = self.movie_manager.retrieve_movies_from_database()
        # print(data_retrieved)
        if data_retrieved:
            for movie_name, movie in data_retrieved.items():
                for copy_id, status in movie.movie_copies.items():
                    self.movies_tree.insert('', tk.END, text=movie_name, values=[copy_id, status])

    def clear_tree(self):
        for items in self.movies_tree.get_children():
            self.movies_tree.delete(items)
