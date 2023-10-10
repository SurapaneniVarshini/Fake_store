import tkinter as tk
import sqlite3
from tkinter import ttk
from datetime import datetime
from fpdf import FPDF
import messagebox

product_window=None

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

def select_product():
    selected_item = tree.focus()
    if selected_item:
        selected_product = tree.item(selected_item)['values']
        product_id = selected_product[0]
        product_description = selected_product[3]
        product_price = selected_product[2]
        show_product_window(product_id, selected_product, product_price)
    else:
        tk.messagebox.showwarning("No Product Selected", "Please select a product from the table.")

def show_product_window(product_id, selected_product, product_price):
    product_window = tk.Toplevel(root)
    product_window.title("Select Product")
    product_window.geometry("300x250")

    # Create labels and entry fields for product details
    product_id_label = tk.Label(product_window, text=f"Product ID: {product_id}")
    product_id_label.pack()

    product_name_label = tk.Label(product_window, text=f"Name: {selected_product[1]}")
    product_name_label.pack()

    price_label = tk.Label(product_window, text=f"Price: ${product_price}")
    price_label.pack()

    description_label = tk.Label(product_window, text=f"Description: {selected_product[3]}")
    description_label.pack()

    quantity_label = tk.Label(product_window, text=f"Quantity:{selected_product[4]}")
    quantity_label.pack()
    quantity_entry = tk.Entry(product_window)
    quantity_entry.pack(pady=10)

    save_button = tk.Button(product_window, text="Save",
                            command=lambda: save_product(product_id, selected_product, product_price, quantity_entry.get()))
    save_button.pack()

def save_product(product_id, selected_product, product_price, quantity):
    try:
        quantity = int(quantity)
        if quantity <= 0:
            messagebox.showwarning("Invalid Quantity", "Please enter a valid quantity.")
            return

        # Connect to the SQLite database
        conn = sqlite3.connect('Store.db')
        cursor = conn.cursor()

        # Retrieve the current available quantity
        cursor.execute('SELECT Quantity FROM Products WHERE ProductID=?', (product_id,))
        current_quantity = cursor.fetchone()[0]

        # Check if the available quantity is sufficient
        if current_quantity < quantity:
            messagebox.showwarning("Insufficient Quantity", "The available quantity is not sufficient.")
            conn.close()
            return

        # Calculate the total price
        total_price = product_price * quantity

        # Update the quantity in the database
        new_quantity = current_quantity - quantity
        cursor.execute('UPDATE Products SET Quantity=? WHERE ProductID=?', (new_quantity, product_id))
        conn.commit()

        # Generate the PDF bill
        generate_bill(product_id, selected_product, quantity, product_price, total_price)

        # Close the database connection
        conn.close()

        # Show success message
        messagebox.showinfo("Success", "Product purchased successfully.")

        # Close the product window
        product_window.destroy()

        # Refresh the table
        retrieve_data()

    except ValueError:
        messagebox.showwarning("Invalid Quantity", "Please enter a valid quantity.")


def generate_bill(product_id, selected_product, quantity, product_price, total_price):
    pdf = FPDF()
    pdf.add_page()

    # Set the font and size for the title
    pdf.set_font("Arial", size=18)

    # Add the store name
    pdf.cell(0, 10, txt="FAKE Store", ln=True, align='C')

    # Set the font and size for the bill content
    pdf.set_font("Arial", size=12)

    # Add the product details
    pdf.cell(0, 10, txt=f"Product ID: {product_id}", ln=True)
    pdf.cell(0, 10, txt=f"Name: {selected_product[1]}", ln=True)
    pdf.cell(0, 10, txt=f"Description: {selected_product[3]}", ln=True)
    pdf.cell(0, 10, txt=f"Quantity: {quantity}", ln=True)
    pdf.cell(0, 10, txt=f"Price: ${product_price}", ln=True)
    pdf.cell(0, 10, txt=f"Total Price: ${total_price}", ln=True)

    # Add the date and time
    pdf.cell(0, 10, txt=datetime.now().strftime("%Y-%m-%d %H:%M:%S"), ln=True)

    # Save the PDF file
    pdf.output("bill.pdf")

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
refresh_btn.pack()

# Create a button to select aApologies for the incomplete response. Here's the continuation and completion of the updated program with the "Select Product" functionality:

select_product_btn = tk.Button(root, text="Select Product", command=select_product)
select_product_btn.pack(pady=10)

# Pack the search elements and treeview widget
search_frame.pack()
tree.pack()

# Start the main event loop
root.mainloop()
