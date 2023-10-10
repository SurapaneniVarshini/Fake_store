import tkinter as tk
from tkinter import messagebox
import sqlite3

def sell_product():
    # Get the values from the entry fields
    product_name = product_name_entry.get()
    price = float(price_entry.get())
    description = description_entry.get()
    quantity = int(quantity_entry.get())

    # Connect to SQLite database
    conn = sqlite3.connect("Store.db")
    cursor = conn.cursor()

    # Get the next available Product ID
    cursor.execute("SELECT MAX(ProductID) FROM Products")
    last_product_id = cursor.fetchone()[0]
    product_id = last_product_id + 1 if last_product_id else 1

    # Insert data into the table
    cursor.execute("INSERT INTO Products (ProductID, ProductName, Price, Description, Quantity) VALUES (?, ?, ?, ?, ?)",
                   (product_id, product_name, price, description, quantity))

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

    messagebox.showinfo("Success", "Product successfully added to the database.")
    window.destroy()

# Create the GUI window
window = tk.Tk()
window.title("Sell Product")
window.geometry("400x300")

# Get the next available Product ID
conn = sqlite3.connect("Store.db")
cursor = conn.cursor()
cursor.execute("SELECT MAX(ProductID) FROM Products")
last_product_id = cursor.fetchone()[0]
product_id = last_product_id + 1 if last_product_id else 1
conn.close()

# Create labels and entry fields
product_id_label = tk.Label(window, text="Product ID:")
product_id_label.pack()
product_id_entry = tk.Entry(window, state='readonly')
product_id_entry.pack()
product_id_entry.configure(state='normal')
product_id_entry.insert(0, product_id)
product_id_entry.configure(state='readonly')

product_name_label = tk.Label(window, text="Product Name:")
product_name_label.pack()
product_name_entry = tk.Entry(window)
product_name_entry.pack()

price_label = tk.Label(window, text="Price:")
price_label.pack()
price_entry = tk.Entry(window)
price_entry.pack()

description_label = tk.Label(window, text="Description:")
description_label.pack()
description_entry = tk.Entry(window)
description_entry.pack()

quantity_label = tk.Label(window, text="Quantity:")
quantity_label.pack()
quantity_entry = tk.Entry(window)
quantity_entry.pack()

# Create the sell button
sell_button = tk.Button(window, text="Sell", command=sell_product)
sell_button.pack(pady=10)

# Run the GUI main loop
window.mainloop()

