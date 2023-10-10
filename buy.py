import tkinter as tk
from tkinter import messagebox
import sqlite3
from datetime import datetime
from fpdf import FPDF
import easygui

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(80)
        self.cell(30, 10, "Bill", 1, 0, 'C')
        self.ln(20)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f"Date and Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", 0, 0, 'C')

def search_product():
    # Get the product ID from the entry field
    product_id = int(product_id_entry.get())

    # Connect to SQLite database
    conn = sqlite3.connect("Store.db")
    cursor = conn.cursor()

    # Retrieve product information
    cursor.execute("SELECT * FROM Products WHERE ProductID=?", (product_id,))
    product = cursor.fetchone()

    if product:
        product_id_label.configure(text="Product ID: " + str(product[0]))
        product_name_label.configure(text="Product Name: " + product[1])
        price_label.configure(text="Price: $" + str(product[2]))
        description_label.configure(text="Description: " + product[3])
        available_quantity_label.configure(text="Available Quantity: " + str(product[4]))
        quantity_entry.delete(0, tk.END)  # Clear the quantity entry field
    else:
        messagebox.showwarning("Product Not Found", "Product ID not found in the database.")

    # Close the database connection
    conn.close()

def save_bill():
    # Get the product ID and quantity from the entry fields
    product_id = int(product_id_entry.get())
    quantity_needed = int(quantity_entry.get())

    # Connect to SQLite database
    conn = sqlite3.connect("Store.db")
    cursor = conn.cursor()

    # Retrieve product information
    cursor.execute("SELECT * FROM Products WHERE ProductID=?", (product_id,))
    product = cursor.fetchone()

    if product:
        # Check if the available quantity is sufficient
        if product[4] >= quantity_needed:
            # Calculate the total price
            total_price = product[2] * quantity_needed

            # Update the available quantity
            new_quantity = product[4] - quantity_needed
            cursor.execute("UPDATE Products SET Quantity=? WHERE ProductID=?", (new_quantity, product_id))
            conn.commit()

            # Generate the bill
            bill = f"Product ID: {product[0]}\n" \
                   f"Description: {product[3]}\n" \
                   f"Quantity Needed: {quantity_needed}\n" \
                   f"Total Price: ${total_price}\n" \
                   f"Date and Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

            # Generate PDF bill
            pdf = PDF()
            pdf.add_page()
            pdf.set_font('Arial', 'B', 12)
            pdf.cell(0, 10, "Bill", ln=True, align='C')
            pdf.set_font('Arial', '', 12)
            pdf.multi_cell(0, 10, bill)
            pdf.output("bill.pdf")

            # Display popup message
            easygui.msgbox("Bought Successfully")

            # Clear the entry fields and labels
            product_id_entry.delete(0, tk.END)
            product_id_label.configure(text="")
            product_name_label.configure(text="")
            price_label.configure(text="")
            description_label.configure(text="")
            available_quantity_label.configure(text="")
            quantity_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Insufficient Quantity",
                                   "The available quantity is not sufficient for the desired quantity.")
    else:
        messagebox.showwarning("Product Not Found", "Product ID not found in the database.")

    # Close the database connection
    conn.close()

# Create the GUI window
window = tk.Tk()
window.title("Buyer")

# Create labels and entry fields
product_id_label = tk.Label(window, text="Product ID:")
product_id_label.pack()
product_id_entry = tk.Entry(window)
product_id_entry.pack()

search_button = tk.Button(window, text="Search", command=search_product)
search_button.pack(pady=5)

product_name_label = tk.Label(window, text="")
product_name_label.pack()

price_label = tk.Label(window, text="")
price_label.pack()

description_label = tk.Label(window, text="")
description_label.pack()

available_quantity_label = tk.Label(window, text="")
available_quantity_label.pack()

quantity_label = tk.Label(window, text="Quantity Needed:")
quantity_label.pack()
quantity_entry = tk.Entry(window)
quantity_entry.pack()

save_button = tk.Button(window, text="Save", command=save_bill)
save_button.pack(pady=10)

# Run the GUI main loop
window.mainloop()
