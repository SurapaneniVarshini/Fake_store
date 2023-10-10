import tkinter as tk
from tkinter import ttk
import sqlite3

def search_order():
    order_id = entry_order_id.get()

    # Connect to the database
    conn = sqlite3.connect('Store.db')
    c = conn.cursor()

    # Execute the query to retrieve order details
    c.execute("SELECT * FROM Orders WHERE OrderID=?", (order_id,))
    results = c.fetchall()

    if len(results) > 0:
        # Create a new window for displaying order details
        order_window = tk.Toplevel(window)
        order_window.title(f"Order Details - OrderID: {order_id}")
        order_window.geometry("600x400")

        # Create a treeview widget to display the order details
        tree = ttk.Treeview(order_window)

        # Define columns
        tree["columns"] = ("ProductName", "Quantity", "TotalPrice")

        # Format columns
        tree.column("#0", width=100, minwidth=100)
        tree.column("ProductName", width=200, minwidth=150)
        tree.column("Quantity", width=100, minwidth=100)
        tree.column("TotalPrice", width=100, minwidth=100)

        # Create column headers
        tree.heading("#0", text="OrderID")
        tree.heading("ProductName", text="Product Name")
        tree.heading("Quantity", text="Quantity")
        tree.heading("TotalPrice", text="Total Price")

        # Initialize total price
        total_price = 0

        # Insert data into the treeview
        for result in results:
            tree.insert("", "end", text=result[0], values=(result[1], result[2], result[3]))
            total_price += result[3]

        # Display the treeview
        tree.pack(fill=tk.BOTH, expand=True)

        # Create a label for total price
        label_total = tk.Label(order_window, text=f"Total Value: {total_price}")
        label_total.pack(side=tk.BOTTOM)

    else:
        tk.messagebox.showinfo("Order Details", "No order found with the given OrderID.")

    # Close the database connection
    conn.close()

# Create the main window
window = tk.Tk()
window.title("Order Details")
window.geometry("300x150")

# Create the label and entry for OrderID
label_order_id = tk.Label(window, text="OrderID:")
label_order_id.pack()

entry_order_id = ttk.Combobox(window, width=15)
entry_order_id.pack()

# Connect to the database
conn = sqlite3.connect('Store.db')
c = conn.cursor()

# Execute the query to retrieve OrderIDs
c.execute("SELECT OrderID FROM Orders")
order_ids = c.fetchall()

# Extract the OrderIDs from the results
order_ids = [order_id[0] for order_id in order_ids]

# Set the OrderIDs as the values for the combobox widget
entry_order_id['values'] = order_ids

# Create the search button
search_button = tk.Button(window, text="Search", command=search_order)
search_button.pack()

# Run the main window loop
window.mainloop()
