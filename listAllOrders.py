import sqlite3
import tkinter as tk
from tkinter import ttk
import pandas as pd

class OrderGUI:
    def __init__(self):
        self.conn = sqlite3.connect('Store.db')
        self.root = tk.Tk()
        self.root.title('Order Data')
        self.root.geometry('800x600')

        self.page_size = 100
        self.current_page = 1
        self.total_pages = 0
        self.orders = []
        self.filtered_orders = []

        self.create_widgets()
        self.load_orders()
        self.display_orders()

        self.root.mainloop()

    def create_widgets(self):
        self.search_frame = tk.Frame(self.root)
        self.search_frame.pack(pady=10)

        self.search_label = tk.Label(self.search_frame, text="Order ID:")
        self.search_label.grid(row=0, column=0, padx=5)

        self.search_entry = tk.Entry(self.search_frame, width=10)
        self.search_entry.grid(row=0, column=1, padx=5)

        self.search_button = tk.Button(self.search_frame, text="Search", command=self.search_orders)
        self.search_button.grid(row=0, column=2, padx=5)

        self.tree_frame = tk.Frame(self.root)
        self.tree_frame.pack(expand=True, fill='both')

        self.treeview = ttk.Treeview(self.tree_frame)

        # Add columns
        headers = ['Order ID', 'Product Name', 'Total Price']
        self.treeview['columns'] = headers
        self.treeview.heading('#0', text='Index')
        self.treeview.column('#0', width=50)
        for header in headers:
            self.treeview.heading(header, text=header)
            self.treeview.column(header, width=150)

        self.treeview.pack(side=tk.LEFT, expand=True, fill='both')

        self.scrollbar = ttk.Scrollbar(self.tree_frame, orient='vertical', command=self.treeview.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill='y')
        self.treeview.configure(yscrollcommand=self.scrollbar.set)

        self.page_frame = tk.Frame(self.root)
        self.page_frame.pack(pady=10)

        self.first_button = tk.Button(self.page_frame, text="First", command=self.first_page, state=tk.DISABLED)
        self.first_button.grid(row=0, column=0, padx=5)

        self.prev_button = tk.Button(self.page_frame, text="Previous", command=self.previous_page, state=tk.DISABLED)
        self.prev_button.grid(row=0, column=1, padx=5)

        self.page_label = tk.Label(self.page_frame, text="")
        self.page_label.grid(row=0, column=2, padx=5)

        self.next_button = tk.Button(self.page_frame, text="Next", command=self.next_page, state=tk.DISABLED)
        self.next_button.grid(row=0, column=3, padx=5)

        self.last_button = tk.Button(self.page_frame, text="Last", command=self.last_page, state=tk.DISABLED)
        self.last_button.grid(row=0, column=4, padx=5)

    def load_orders(self):
        query = "SELECT * FROM orders"
        df = pd.read_sql_query(query, self.conn)

        self.orders = df.values.tolist()
        self.filtered_orders = self.orders
        self.total_pages = (len(self.filtered_orders) - 1) // self.page_size + 1
        self.current_page = 1

    def display_orders(self):
        self.clear_table()

        start_index = (self.current_page - 1) * self.page_size
        end_index = start_index + self.page_size
        current_orders = self.filtered_orders[start_index:end_index]

        for i, row in enumerate(current_orders, start=start_index + 1):
            self.treeview.insert(parent='', index='end', iid=i, text=str(i), values=row)

        self.page_label.configure(text=f"Page {self.current_page} of {self.total_pages}")

        if self.current_page > 1:
            self.first_button.configure(state=tk.NORMAL)
            self.prev_button.configure(state=tk.NORMAL)
        else:
            self.first_button.configure(state=tk.DISABLED)
            self.prev_button.configure(state=tk.DISABLED)

        if self.current_page < self.total_pages:
            self.next_button.configure(state=tk.NORMAL)
            self.last_button.configure(state=tk.NORMAL)
        else:
            self.next_button.configure(state=tk.DISABLED)
            self.last_button.configure(state=tk.DISABLED)

    def clear_table(self):
        self.treeview.delete(*self.treeview.get_children())

    def first_page(self):
        if self.current_page > 1:
            self.current_page = 1
            self.display_orders()

    def previous_page(self):
        if self.current_page > 1:
            self.current_page -= 1
            self.display_orders()

    def next_page(self):
        if self.current_page < self.total_pages:
            self.current_page += 1
            self.display_orders()

    def last_page(self):
        if self.current_page < self.total_pages:
            self.current_page = self.total_pages
            self.display_orders()

    def search_orders(self):
        order_id = self.search_entry.get()

        if order_id:
            self.filtered_orders = [order for order in self.orders if str(order[0]) == order_id]
        else:
            self.filtered_orders = self.orders

        self.total_pages = (len(self.filtered_orders) - 1) // self.page_size + 1
        self.current_page = 1
        self.display_orders()

OrderGUI()
