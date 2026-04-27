import tkinter as tk
from tkinter import messagebox
import mysql.connector

# 🔹 Connect to MySQL
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Enter_Your_Password",
    database="DoveStoryDB"
)

cursor = db.cursor()

# 🔹 Add Customer
def add_customer():
    name = entry_name.get()
    phone = entry_phone.get()

    if name == "" or phone == "":
        messagebox.showerror("Error", "Fill all fields")
        return

    query = "INSERT INTO Customers (Name, Phone) VALUES (%s, %s)"
    cursor.execute(query, (name, phone))
    db.commit()

    messagebox.showinfo("Success", "Customer Added")

    entry_name.delete(0, tk.END)
    entry_phone.delete(0, tk.END)

# 🔹 View Customers
def view_customers():
    cursor.execute("SELECT * FROM Customers")
    rows = cursor.fetchall()

    text_box.delete("1.0", tk.END)

    for row in rows:
        text_box.insert(tk.END, str(row) + "\n")

# 🔹 UI Window
root = tk.Tk()
root.title("Dove Story UI")

tk.Label(root, text="Name").pack()
entry_name = tk.Entry(root)
entry_name.pack()

tk.Label(root, text="Phone").pack()
entry_phone = tk.Entry(root)
entry_phone.pack()

tk.Button(root, text="Add Customer", command=add_customer).pack(pady=5)
tk.Button(root, text="View Customers", command=view_customers).pack(pady=5)

text_box = tk.Text(root, height=10, width=40)
text_box.pack()

root.mainloop()
