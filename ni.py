import tkinter as tk
from tkinter import messagebox
import sqlite3

def update_product(product_id, name, price):
    if name and price:
        conn = sqlite3.connect('Store.db')
        cursor = conn.cursor()
        cursor.execute('UPDATE Products SET Name=?, Price=? WHERE "Product ID"=?', (name, price, product_id))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Product updated successfully.")
    else:
        messagebox.showerror("Error", "Please enter both name and price.")

def open_update_window(product):
    def apply_update():
        name = name_entry.get()
        price = price_entry.get()
        update_product(product[0], name, price)
        new_window.destroy()

    new_window = tk.Toplevel()
    new_window.title("Update Product")

    name_label = tk.Label(new_window, text="Name:")
    name_label.grid(row=0, column=0, padx=10, pady=5, sticky=tk.E)
    name_entry = tk.Entry(new_window, width=30)
    name_entry.grid(row=0, column=1, padx=10, pady=5)
    name_entry.insert(0, product[1])

    price_label = tk.Label(new_window, text="Price:")
    price_label.grid(row=1, column=0, padx=10, pady=5, sticky=tk.E)
    price_entry = tk.Entry(new_window, width=30)
    price_entry.grid(row=1, column=1, padx=10, pady=5)
    price_entry.insert(0, product[2])

    update_button = tk.Button(new_window, text="Update", command=apply_update)
    update_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

if __name__ == "__main__":
    selected_product_id = "1"  # Replace with the actual product ID
    conn = sqlite3.connect('Store.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Products WHERE "Product ID"=?', (selected_product_id,))
    product = cursor.fetchone()
    conn.close()

    if product:
        open_update_window(product)
    else:
        messagebox.showerror("Error", "Product not found.")
