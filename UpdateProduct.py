import sqlite3
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

class ProductGUI:
    def __init__(self):
        self.conn = sqlite3.connect('Store.db')
        self.cursor = self.conn.cursor()

        self.root = tk.Tk()
        self.root.title('Product Management')

        self.create_widgets()
        self.load_products()
        self.display_products()

        self.root.mainloop()

    def create_widgets(self):
        self.tree_frame = tk.Frame(self.root)
        self.tree_frame.pack(expand=True, fill='both')

        self.treeview = ttk.Treeview(self.tree_frame)
        self.treeview.pack(side=tk.LEFT, expand=True, fill='both')

        self.scrollbar = ttk.Scrollbar(self.tree_frame, orient='vertical', command=self.treeview.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill='y')
        self.treeview.configure(yscrollcommand=self.scrollbar.set)

        self.treeview['columns'] = ('Product ID', 'Name', 'Price', 'Description', 'Quantity')
        self.treeview.heading('#0', text='Index')
        self.treeview.column('#0', width=50)
        headers = ['Product ID', 'Name', 'Price', 'Description', 'Quantity']
        for i, header in enumerate(headers, start=1):
            self.treeview.heading(header, text=header)
            self.treeview.column(header, width=150)

        self.delete_button = tk.Button(self.root, text='Delete', command=self.delete_product)
        self.delete_button.pack(pady=5)

        self.update_button = tk.Button(self.root, text='Update', command=self.open_update_window)
        self.update_button.pack(pady=5)

    def load_products(self):
        self.cursor.execute('SELECT * FROM Products')
        self.products = self.cursor.fetchall()

    def display_products(self):
        self.clear_table()
        for i, product in enumerate(self.products, start=1):
            self.treeview.insert('', 'end', iid=i, text=str(i), values=product)

    def clear_table(self):
        self.treeview.delete(*self.treeview.get_children())

    def delete_product(self):
        selected_item = self.treeview.selection()
        if selected_item:
            product_id = self.treeview.set(selected_item, 'Product ID')
            confirmation = messagebox.askyesno('Confirmation', f'Do you want to delete Product ID: {product_id}?')
            if confirmation:
                self.cursor.execute('DELETE FROM Products WHERE "ProductID"=?', (product_id,))
                self.conn.commit()
                self.load_products()
                self.display_products()
                messagebox.showinfo('Success', f'Product ID: {product_id} deleted successfully.')

    def open_update_window(self):
        selected_item = self.treeview.selection()
        if selected_item:
            selected_product = self.treeview.item(selected_item)
            product_id = selected_product['values'][0]
            self.cursor.execute('SELECT * FROM Products WHERE "ProductID"=?', (product_id,))
            product = self.cursor.fetchone()

            if product:
                update_window = tk.Toplevel(self.root)
                update_window.title('Update Product')

                product_id_label = tk.Label(update_window, text='Product ID:')
                product_id_label.grid(row=0, column=0, padx=10, pady=5, sticky=tk.E)
                product_id_entry = tk.Entry(update_window, state='readonly')
                product_id_entry.grid(row=0, column=1, padx=10, pady=5)
                product_id_entry.insert(0, product[0])

                name_label = tk.Label(update_window, text='Name:')
                name_label.grid(row=1, column=0, padx=10, pady=5, sticky=tk.E)
                name_entry = tk.Entry(update_window, width=30)
                name_entry.grid(row=1, column=1, padx=10, pady=5)
                name_entry.insert(0, product[1])

                price_label = tk.Label(update_window, text='Price:')
                price_label.grid(row=2, column=0, padx=10, pady=5, sticky=tk.E)
                price_entry = tk.Entry(update_window, width=30)
                price_entry.grid(row=2, column=1, padx=10, pady=5)
                price_entry.insert(0, product[2])

                description_label = tk.Label(update_window, text='Description:')
                description_label.grid(row=3, column=0, padx=10, pady=5, sticky=tk.E)
                description_entry = tk.Entry(update_window, width=30)
                description_entry.grid(row=3, column=1, padx=10, pady=5)
                description_entry.insert(0, product[3])

                quantity_label = tk.Label(update_window, text='Quantity:')
                quantity_label.grid(row=4, column=0, padx=10, pady=5, sticky=tk.E)
                quantity_entry = tk.Entry(update_window, width=30)
                quantity_entry.grid(row=4, column=1, padx=10, pady=5)
                quantity_entry.insert(0, product[4])

                update_button = tk.Button(update_window, text='Update', command=lambda: self.update_product(
                    product_id, name_entry.get(), price_entry.get(), description_entry.get(), quantity_entry.get()))
                update_button.grid(row=5, column=0, columnspan=2, padx=10, pady=10)
            else:
                messagebox.showerror('Error', 'Product not found.')

    def update_product(self, product_id, name, price, description, quantity):
        if name and price and description and quantity:
            confirmation = messagebox.askyesno('Confirmation', 'Do you want to update the product?')
            if confirmation:
                self.cursor.execute('UPDATE Products SET ProductName=?, Price=?, Description=?, Quantity=? WHERE "ProductID"=?',
                                    (name, price, description, quantity, product_id))
                self.conn.commit()
                self.load_products()
                self.display_products()
                messagebox.showinfo('Success', 'Product updated successfully.')
        else:
            messagebox.showerror('Error', 'Please enter all the details.')

ProductGUI()
