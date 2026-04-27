# Restaurant-Management-Database
This project develops a Restaurant Management Database System for “The Dove Story”. It manages customer details, orders, delivery assignments, and menu items using a relational database.


# 🍽️ Dove Story Restaurant Management System

A simple restaurant management system built using **MySQL and Python (Tkinter UI)**.  
This project demonstrates database design, relationships using foreign keys, and a basic graphical interface for interacting with the database.

---

## 🚀 Features

- Add new customers
- Place orders using dropdown selection
- View customer data
- Relational database with proper table connections
- Simple Python GUI for interaction

---

## 🛠️ Tech Stack

- **Database:** MySQL  
- **Backend Logic:** Python  
- **UI:** Tkinter  
- **Tools:** PyCharm, MySQL Workbench  

---

## 🗂️ Database Structure

The system includes the following tables:

- **Customers** (CustomerID, Name, Phone)  
- **DeliveryBoy** (DeliveryBoyID, Name)  
- **MenuItem** (ItemID, Name, Price)  
- **Orders** (OrderID, CustomerID, DeliveryBoyID)  
- **OrderItem** (OrderItemID, OrderID, ItemID, Quantity)  

Relationships:
- One customer → many orders  
- One delivery boy → many orders  
- One order → multiple items  

---

## ▶️ How to Run

### 1. Setup Database
- Open MySQL Workbench
- Create database:
