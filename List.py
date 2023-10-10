import tkinter as tk
import sqlite3
from tkinter import ttk

# Create a function to retrieve data from the database
def retrieve_data():
    # Connect to the SQLite database
    conn = sqlite3.connect('Store.db')
    cursor = conn.cursor()

    # Retrieve all data from the Products table
    cursor.execute('SELECT * FROM Products')
    data = cursor.fetchall()

    # Close the database connection
    conn.close()

    # Clear any previous data in the table
    for i in tree.get_children():
        tree.delete(i)

    # Insert the retrieved data into the table
    for row in data:
        tree.insert('', 'end', values=row)

def search_product():
    # Get the product ID from the entry field
    product_id = int(search_entry.get())

    # Connect to the SQLite database
    conn = sqlite3.connect('Store.db')
    cursor = conn.cursor()

    # Retrieve the product with the specified ID
    cursor.execute('SELECT * FROM Products WHERE ProductID=?', (product_id,))
    product = cursor.fetchone()

    # Clear the table
    for i in tree.get_children():
        tree.delete(i)

    # Display the product if found
    if product:
        tree.insert('', 'end', values=product)

    # Close the database connection
    conn.close()

# Create the main window
root = tk.Tk()
root.title("Product List")

# Create a search frame
search_frame = tk.Frame(root)
search_frame.pack(pady=10)

# Create a label and entry field for the search
search_label = tk.Label(search_frame, text="Search Product ID:")
search_label.pack(side=tk.LEFT)
search_entry = tk.Entry(search_frame, width=10)
search_entry.pack(side=tk.LEFT, padx=5)
search_button = tk.Button(search_frame, text="Search", command=search_product)
search_button.pack(side=tk.LEFT)

# Create a treeview widget to display the data
tree = ttk.Treeview(root, columns=('ProductID', 'Name', 'Price', 'Description', 'Quantity'), show='headings')

# Define the column headings
tree.heading('ProductID', text='Product ID')
tree.heading('Name', text='Name')
tree.heading('Price', text='Price')
tree.heading('Description', text='Description')
tree.heading('Quantity', text='Quantity')

# Define the column widths
tree.column('ProductID', width=80)
tree.column('Name', width=150)
tree.column('Price', width=80)
tree.column('Description', width=200)
tree.column('Quantity', width=80)

# Retrieve and insert data into the table
retrieve_data()

# Create a button to refresh the data
refresh_btn = tk.Button(root, text="Refresh", command=retrieve_data)

# Pack the search elements, treeview widget, and refresh button
search_frame.pack()
tree.pack()
refresh_btn.pack()

# Start the main event loop
root.mainloop()
