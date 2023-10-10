import tkinter as tk
import subprocess

def buy_button_click():
    subprocess.run(["python", "FAKE4.py"])

def list_button_click():
    subprocess.run(["python", "sell.py"])

def listAllProducts():
    subprocess.run(["python","List.py"])
def manageProducts():
    subprocess.run(["python","UpdateProduct.py"])

# Create the main window
window = tk.Tk()
window.title("GUI Example")
window.geometry("600x600")

# Create the Buy button
buy_button = tk.Button(window, text="Buy", command=buy_button_click)
buy_button.pack(pady=10)

# Create the List button
list_button = tk.Button(window, text="Sell Item", command=list_button_click)
list_button.pack(pady=10)

list_button = tk.Button(window, text="List ALL Products", command=listAllProducts)
list_button.pack(pady=10)

list_button = tk.Button(window, text="Manage Products", command=manageProducts)
list_button.pack(pady=10)

# Start the GUI event loop
window.mainloop()
