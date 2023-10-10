import sqlite3
from tkinter import *
import subprocess

def login_user():
    username = entry_username.get()
    password = entry_password.get()

    conn = sqlite3.connect('Store.db')
    cursor = conn.cursor()

    # Check if the username and password match in the UsersTable
    cursor.execute("SELECT UserId FROM Users WHERE Username = ? AND Password = ?", (username, password))
    result = cursor.fetchone()

    conn.close()

    if result:
        root.destroy()  # Close the login window
        open_list_py()  # Open the "List.py" file
    else:
        print("Invalid username or password!")

def open_list_py():
    subprocess.Popen(["python", "welcome.py"])

# GUI setup
root = Tk()
root.title("User Login")

label_username = Label(root, text="Username:")
label_username.pack()
entry_username = Entry(root)
entry_username.pack()

label_password = Label(root, text="Password:")
label_password.pack()
entry_password = Entry(root, show="*")
entry_password.pack()

button_login = Button(root, text="Login", command=login_user)
button_login.pack()

root.mainloop()
