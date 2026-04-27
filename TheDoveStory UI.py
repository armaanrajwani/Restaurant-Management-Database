import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import mysql.connector

# 🔹 DB CONNECTION
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Password",
    database="DoveStoryDB"
)

# 🔥 IMPORTANT FIX
cursor = db.cursor(buffered=True)

# 🔹 LOAD CUSTOMERS
def load_customers():
    cursor.execute("SELECT CustomerID, Name FROM Customers")
    rows = cursor.fetchall()
    customer_combo['values'] = [f"{r[0]} - {r[1]}" for r in rows]

# 🔹 ADD CUSTOMER
def add_customer():
    name = entry_name.get()
    phone = entry_phone.get()

    if not name or not phone:
        messagebox.showerror("Error", "Fill all fields")
        return

    cursor.execute(
        "INSERT INTO Customers (Name, Phone) VALUES (%s, %s)",
        (name, phone)
    )
    db.commit()

    messagebox.showinfo("Success", "Customer Added")

    entry_name.delete(0, tk.END)
    entry_phone.delete(0, tk.END)

    load_customers()

# 🔹 PLACE ORDER
def place_order():
    try:
        if not customer_combo.get():
            messagebox.showerror("Error", "Select Customer")
            return

        if not delivery_combo.get():
            messagebox.showerror("Error", "Select Delivery Boy")
            return

        if not item_combo.get():
            messagebox.showerror("Error", "Select Item")
            return

        quantity = int(quantity_combo.get())
        if quantity == 0:
            messagebox.showerror("Error", "Quantity must be > 0")
            return

        # Extract IDs
        customer_id = int(customer_combo.get().split(" - ")[0])

        # Get DeliveryBoyID
        cursor.execute(
            "SELECT DeliveryBoyID FROM DeliveryBoy WHERE Name=%s",
            (delivery_combo.get(),)
        )
        delivery = cursor.fetchone()
        if not delivery:
            messagebox.showerror("Error", "Delivery boy not found")
            return
        delivery_id = delivery[0]

        # Get ItemID
        cursor.execute(
            "SELECT ItemID FROM MenuItem WHERE Name=%s",
            (item_combo.get(),)
        )
        item = cursor.fetchone()
        if not item:
            messagebox.showerror("Error", "Item not found")
            return
        item_id = item[0]

        # Insert Order
        cursor.execute(
            "INSERT INTO Orders (CustomerID, DeliveryBoyID) VALUES (%s, %s)",
            (customer_id, delivery_id)
        )
        db.commit()

        order_id = cursor.lastrowid

        # Insert OrderItem
        cursor.execute(
            "INSERT INTO OrderItem (OrderID, ItemID, Quantity) VALUES (%s, %s, %s)",
            (order_id, item_id, quantity)
        )
        db.commit()

        messagebox.showinfo("Success", "Order Placed!")

    except Exception as e:
        messagebox.showerror("Error", str(e))

# 🔹 VIEW ALL DATA
def view_all():
    query = """
    SELECT 
        o.OrderID,
        c.Name,
        d.Name,
        m.Name,
        oi.Quantity
    FROM Orders o
    JOIN Customers c ON o.CustomerID = c.CustomerID
    JOIN DeliveryBoy d ON o.DeliveryBoyID = d.DeliveryBoyID
    JOIN OrderItem oi ON o.OrderID = oi.OrderID
    JOIN MenuItem m ON oi.ItemID = m.ItemID
    ORDER BY o.OrderID;
    """

    cursor.execute(query)
    rows = cursor.fetchall()

    text_box.delete("1.0", tk.END)

    text_box.insert(tk.END, "OrderID | Customer | Delivery | Item | Qty\n")
    text_box.insert(tk.END, "-" * 50 + "\n")

    for row in rows:
        text_box.insert(tk.END, f"{row[0]} | {row[1]} | {row[2]} | {row[3]} | {row[4]}\n")

# 🔹 UI
root = tk.Tk()
root.title("Dove Story UI")
root.geometry("400x550")

# 🔹 ADD CUSTOMER
tk.Label(root, text="Add Customer", font=("Arial", 12, "bold")).pack(pady=5)

entry_name = tk.Entry(root)
entry_name.pack(pady=5)

entry_phone = tk.Entry(root)
entry_phone.pack(pady=5)

tk.Button(root, text="Add Customer", command=add_customer).pack(pady=5)

# 🔹 ORDER SECTION
tk.Label(root, text="Place Order", font=("Arial", 12, "bold")).pack(pady=10)

customer_combo = ttk.Combobox(root)
customer_combo.pack(pady=5)

delivery_combo = ttk.Combobox(root, values=["Alpha", "Bravo"])
delivery_combo.pack(pady=5)

item_combo = ttk.Combobox(root, values=["Pizza", "Burger"])
item_combo.pack(pady=5)

quantity_combo = ttk.Combobox(root, values=[0,1,2,3])
quantity_combo.pack(pady=5)

tk.Button(root, text="Place Order", command=place_order).pack(pady=5)

# 🔹 VIEW DATA
tk.Button(root, text="View All Orders", command=view_all).pack(pady=10)

text_box = tk.Text(root, height=12, width=45)
text_box.pack()

# 🔹 INITIAL LOAD
load_customers()

root.mainloop()
