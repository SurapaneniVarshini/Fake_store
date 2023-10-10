import tkinter as tk
import sqlite3
from tkinter import ttk
from datetime import datetime
from fpdf import FPDF
from tkinter import messagebox

product_window = None
cart = []

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
    global product_window
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

    quantity_label = tk.Label(product_window, text=f"Quantity available:{selected_product[4]}")
    quantity_label.pack()
    quantity_entry = tk.Entry(product_window)
    quantity_entry.pack(pady=10)

    add_to_cart_button = tk.Button(product_window, text="Add to Cart",
                                   command=lambda: add_to_cart(product_id, selected_product, product_price, quantity_entry.get()))
    add_to_cart_button.pack()

def add_to_cart(product_id, selected_product, product_price, quantity):
    try:
        quantity = int(quantity)
        if quantity <= 0:
            messagebox.showwarning("Invalid Quantity", "Please enter a valid quantity.")
            return

        # Check if the available quantity is sufficient
        if selected_product[4] < quantity:
            messagebox.showwarning("Insufficient Quantity", "The available quantity is not sufficient.")
            return

        # Add the product to the cart
        product = {
            'product_id': product_id,
            'name': selected_product[1],
            'price': product_price,
            'quantity': quantity
        }
        cart.append(product)

        # Show success message
        messagebox.showinfo("Success", "Product added to cart.")

        # Close the product window
        product_window.destroy()

    except ValueError:
        messagebox.showwarning("Invalid Quantity", "Please enter a valid quantity.")

def view_cart():
    if not cart:
        messagebox.showinfo("Empty Cart", "The cart is empty.")
    else:
        cart_window = tk.Toplevel(root)
        cart_window.title("Cart")
        cart_window.geometry("300x250")

        cart_label = tk.Label(cart_window, text="Cart:")
        cart_label.pack()

        total_price = 0  # Variable to store the total price

        for product in cart:
            product_label = tk.Label(cart_window, text=f"Product: {product['name']}, Quantity: {product['quantity']}")
            product_label.pack()

            # Calculate the subtotal for the product
            subtotal = float(product['price']) * product['quantity']
            total_price += subtotal

            subtotal_label = tk.Label(cart_window, text=f"Subtotal: ${subtotal:.2f}")
            subtotal_label.pack()

        # Display the total price
        total_price_label = tk.Label(cart_window, text=f"Total Price: ${total_price:.2f}")
        total_price_label.pack()


def checkout():
    if not cart:
        messagebox.showwarning("Empty Cart", "The cart is empty. Please add products to the cart.")
        return

    # Connect to the SQLite database
    conn = sqlite3.connect('Store.db')
    cursor = conn.cursor()

    try:
        # Calculate total price
        total_price = sum(float(product['price']) * product['quantity'] for product in cart)

        # Update quantity in the database and generate the PDF bill
        for product in cart:
            product_id = product['product_id']
            quantity = product['quantity']

            # Retrieve the current available quantity
            cursor.execute('SELECT Quantity FROM Products WHERE ProductID=?', (product_id,))
            current_quantity = cursor.fetchone()[0]

            # Check if the available quantity is sufficient
            if current_quantity < quantity:
                messagebox.showwarning("Insufficient Quantity", f"The available quantity for Product ID {product_id} is not sufficient.")
                return

            # Update the quantity in the database
            new_quantity = current_quantity - quantity
            cursor.execute('UPDATE Products SET Quantity=? WHERE ProductID=?', (new_quantity, product_id))
            conn.commit()

        # Generate the PDF bill
        generate_bill(cart, total_price)

        # Clear the cart
        cart.clear()

        # Show the success message
        messagebox.showinfo("Success", "Checkout successful. Cart cleared.")

        # Refresh the table
        retrieve_data()

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred during checkout: {str(e)}")

    finally:
        # Close the database connection
        conn.close()



def generate_bill(cart, total_price):
    pdf = FPDF()
    pdf.add_page()

    # Set the font and size for the title
    pdf.set_font("Arial", size=18)

    # Add the store name
    pdf.cell(0, 10, txt="FAKE Store", ln=True, align='C')

    # Set the font and size for the bill content
    pdf.set_font("Arial", size=12)

    # Add the cart details
    for product in cart:
        pdf.cell(0, 10, txt=f"Product ID: {product['product_id']}", ln=True)
        pdf.cell(0, 10, txt=f"Name: {product['name']}", ln=True)
        pdf.cell(0, 10, txt=f"Quantity: {product['quantity']}", ln=True)
        pdf.cell(0, 10, txt=f"Price: ${product['price']}", ln=True)
        pdf.cell(0, 10, ln=True)

    # Add the total price
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

# Create a button to select a product
select_product_btn = tk.Button(root, text="Select Product", command=select_product)
select_product_btn.pack(pady=10)

# Create a button to view the cart
view_cart_btn = tk.Button(root, text="View Cart", command=view_cart)
view_cart_btn.pack()

# Create a button to checkout
checkout_btn = tk.Button(root, text="Checkout", command=checkout)
checkout_btn.pack()

# Pack the search elements and treeview widget
search_frame.pack()
tree.pack()

# Start the main event loop
root.mainloop()
