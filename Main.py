import tkinter as tk
from tkinter import messagebox
import subprocess

def login():
    subprocess.call(["python", "Login.py"])

def register():
    subprocess.call(["python", "Register.py"])

def center_window(window):
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    x = (window.winfo_screenwidth() // 2) - (width // 2)
    y = (window.winfo_screenheight() // 2) - (height // 2)
    window.geometry('{}x{}+{}+{}'.format(width, height, x, y))

window = tk.Tk()
window.title("Fake Store")
window.geometry("300x100")

center_window(window)

login_button = tk.Button(window, text="Login", command=login)
login_button.pack(pady=10)

register_button = tk.Button(window, text="Register", command=register)
register_button.pack(pady=5)

window.mainloop()
