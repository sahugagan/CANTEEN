import tkinter as tk
from tkinter import messagebox, simpledialog
import sqlite3
from playsound import playsound

# Connect to the SQLite database or create it if it doesn't exist
conn = sqlite3.connect('restaurant.db')
cursor = conn.cursor()

# Create the "employees" table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS employees (
        user_id TEXT PRIMARY KEY,
        password TEXT
    )
''')
conn.commit()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS menu (
        item_id INTEGER PRIMARY KEY,
        item_name TEXT,
        price REAL,
        quantity INTEGER
    )
''')
conn.commit()

# Global variables
cart_items = []

# Function to maximize a window
def maximize_window(window):
    window.state('zoomed')

# Function to open the main admin dashboard
def open_admin_dashboard():
    admin_dashboard_window = tk.Toplevel(root)
    admin_dashboard_window.title("Admin Dashboard")
    maximize_window(admin_dashboard_window)

    center_frame = tk.Frame(admin_dashboard_window, bg="#f0f0f0", bd=5)
    center_frame.pack(expand=True, padx=20, pady=20)

    create_menu_button = tk.Button(center_frame, text="Create Menu", bg="#4CAF50", fg="white", font=("Arial", 14, "bold"), command=open_create_menu)
    create_menu_button.pack(pady=10)

    menu_button = tk.Button(center_frame, text="Menu", bg="#1E90FF", fg="white", font=("Arial", 14, "bold"), command=show_menu)
    menu_button.pack(pady=10)

    cart_button = tk.Button(center_frame, text="View Cart", bg="#FFD700", fg="black", font=("Arial", 14, "bold"), command=show_cart)
    cart_button.pack(pady=10)

    logout_button = tk.Button(center_frame, text="Log Out", bg="#FF6347", fg="white", font=("Arial", 14, "bold"), command=root.quit)
    logout_button.pack(pady=10)

# Function to open the Create Menu window
def open_create_menu():
    create_menu_window = tk.Toplevel(root)
    create_menu_window.title("Create Menu")
    maximize_window(create_menu_window)

    center_frame = tk.Frame(create_menu_window, bg="#f0f0f0", bd=5)
    center_frame.pack(expand=True, padx=20, pady=20)

    item_name_label = tk.Label(center_frame, text="Item Name:", font=("Arial", 14), bg="#f0f0f0", fg="#333")
    item_name_label.pack()

    item_name_entry = tk.Entry(center_frame, font=("Arial", 12))
    item_name_entry.pack()

    price_label = tk.Label(center_frame, text="Price:", font=("Arial", 14), bg="#f0f0f0", fg="#333")
    price_label.pack()

    price_entry = tk.Entry(center_frame, font=("Arial", 12))
    price_entry.pack()

    quantity_label = tk.Label(center_frame, text="Quantity:", font=("Arial", 14), bg="#f0f0f0", fg="#333")
    quantity_label.pack()

    quantity_var = tk.IntVar()
    quantity_spinbox = tk.Spinbox(center_frame, from_=1, to=100, font=("Arial", 12), textvariable=quantity_var)
    quantity_spinbox.pack()

    def add_to_menu():
        item_name = item_name_entry.get()
        price = price_entry.get()
        quantity = quantity_var.get()

        if not item_name or not price:
            messagebox.showerror("Error", "Please fill in all fields.")
        else:
            # Check if the item already exists in the menu
            cursor.execute('SELECT * FROM menu WHERE item_name=?', (item_name,))
            existing_item = cursor.fetchone()

            if existing_item:
                messagebox.showerror("Error", f"Item {item_name} already exists in the menu.")
            else:
                cursor.execute('INSERT INTO menu (item_name, price, quantity) VALUES (?, ?, ?)', (item_name, price, quantity))
                conn.commit()
                messagebox.showinfo("Success", f"Item {item_name} added to menu successfully!")

    add_to_menu_button = tk.Button(center_frame, text="Add to Menu", bg="#1E90FF", fg="white", font=("Arial", 14, "bold"), command=add_to_menu)
    add_to_menu_button.pack(pady=10)

# Function to show the menu
# Function to show the menu
def show_menu():
    menu_window = tk.Toplevel(root)
    menu_window.title("Menu")
    maximize_window(menu_window)

    def delete_item(item_id):
        cursor.execute('DELETE FROM menu WHERE item_id = ?', (item_id,))
        conn.commit()
        messagebox.showinfo("Success", "Item deleted from menu successfully!")
        menu_window.destroy()  # Close the menu window after deleting

    def add_to_cart(item, quantity_var):
        item_name = item[1]
        price = item[2]
        quantity = quantity_var.get()
        cart_items.append((item_name, price, quantity))
        messagebox.showinfo("Success", "Item added to cart successfully!")

    center_frame = tk.Frame(menu_window, bg="#f0f0f0", bd=5)
    center_frame.pack(expand=True, padx=20, pady=20)

    cursor.execute('SELECT * FROM menu')
    menu_items = cursor.fetchall()

    if menu_items:
        for item in menu_items:
            item_frame = tk.Frame(center_frame, bg="#f0f0f0", bd=2, relief="groove")
            item_frame.pack(fill="x", padx=10, pady=5)

            item_label = tk.Label(item_frame, text=f"Item Name: {item[1]}", font=("Arial", 14), bg="#f0f0f0", fg="#333")
            item_label.pack(side="left", padx=10, pady=5)

            price_label = tk.Label(item_frame, text=f"Price: ${item[2]}", font=("Arial", 14), bg="#f0f0f0", fg="#333")
            price_label.pack(side="left", padx=10, pady=5)

            quantity_label = tk.Label(item_frame, text=f"Quantity:", font=("Arial", 14), bg="#f0f0f0", fg="#333")
            quantity_label.pack(side="left", padx=10, pady=5)

            quantity_var = tk.IntVar()
            quantity_spinbox = tk.Spinbox(item_frame, from_=1, to=100, font=("Arial", 12), textvariable=quantity_var)
            quantity_spinbox.pack(side="left", padx=10, pady=5)

            add_to_cart_button = tk.Button(item_frame, text="Add to Cart", bg="#1E90FF", fg="white", font=("Arial", 12), command=lambda item=item, quantity_var=quantity_var: add_to_cart(item, quantity_var))
            add_to_cart_button.pack(side="right", padx=10, pady=5)

            delete_button = tk.Button(item_frame, text="Delete", bg="#FF6347", fg="white", font=("Arial", 12), command=lambda item_id=item[0]: delete_item(item_id))
            delete_button.pack(side="right", padx=10, pady=5)
    else:
        no_item_label = tk.Label(center_frame, text="No items in the menu yet.", font=("Arial", 14), bg="#f0f0f0", fg="#333")
        no_item_label.pack()





# Function to show the cart
def show_cart():
    cart_window = tk.Toplevel(root)
    cart_window.title("Cart")
    maximize_window(cart_window)

    cart_frame = tk.Frame(cart_window, bg="#f0f0f0", bd=5)
    cart_frame.pack(expand=True, padx=20, pady=20)

    if cart_items:
        for item in cart_items:
            item_frame = tk.Frame(cart_frame, bg="#f0f0f0", bd=2, relief="groove")
            item_frame.pack(fill="x", padx=10, pady=5)

            item_label = tk.Label(item_frame, text=f"Item Name: {item[0]}", font=("Arial", 14), bg="#f0f0f0", fg="#333")
            item_label.pack(side="left", padx=10, pady=5)

            price_label = tk.Label(item_frame, text=f"Price: ${item[1]}", font=("Arial", 14), bg="#f0f0f0", fg="#333")
            price_label.pack(side="left", padx=10, pady=5)

            quantity_label = tk.Label(item_frame, text=f"Quantity: {item[2]}", font=("Arial", 14), bg="#f0f0f0", fg="#333")
            quantity_label.pack(side="left", padx=10, pady=5)

            remove_button = tk.Button(item_frame, text="Remove", bg="#FF6347", fg="white", font=("Arial", 12), command=lambda item=item: remove_from_cart(item))
            remove_button.pack(side="right", padx=10, pady=5)
    else:
        no_item_label = tk.Label(cart_frame, text="Your cart is empty.", font=("Arial", 14), bg="#f0f0f0", fg="#333")
        no_item_label.pack()

    generate_bill_button = tk.Button(cart_frame, text="Generate Bill", bg="#1E90FF", fg="white", font=("Arial", 14, "bold"), command=generate_bill)
    generate_bill_button.pack(pady=20, ipadx=10)

# Function to remove items from the cart
def remove_from_cart(item):
    cart_items.remove(item)
    show_cart()

# Function to generate and display the bill
def generate_bill():
    if not cart_items:
        messagebox.showerror("Error", "Your cart is empty.")
    else:
        total_price = sum(item[1] * item[2] for item in cart_items)
        bill_window = tk.Toplevel(root)
        bill_window.title("Bill")
        maximize_window(bill_window)

        bill_frame = tk.Frame(bill_window, bg="#f0f0f0", bd=5)
        bill_frame.pack(expand=True, padx=20, pady=20)

        for index, item in enumerate(cart_items, start=1):
            item_label = tk.Label(bill_frame, text=f"Item {index}: {item[0]} | Price: ${item[1]} | Quantity: {item[2]}", font=("Arial", 14), bg="#f0f0f0", fg="#333")
            item_label.pack(side="top", padx=10, pady=5)

        total_label = tk.Label(bill_frame, text=f"Total Price: ${total_price}", font=("Arial", 16, "bold"), bg="#f0f0f0", fg="#333")
        total_label.pack(pady=20)

        print_bill_button = tk.Button(bill_frame, text="Print Bill", bg="#4CAF50", fg="white", font=("Arial", 14, "bold"), command=lambda: print_bill(bill_window))
        print_bill_button.pack(pady=10, ipadx=10)

def print_bill(window):
    confirm_print = simpledialog.askstring("Print Bill", "Do you want to print the bill? (yes/no)")
    if confirm_print and confirm_print.lower() == 'yes':
        window.update_idletasks()  # Update idle tasks before printing
        window.attributes('-topmost', 0)  # Set the window to normal state
        window.attributes('-topmost', 1)  # Bring the window to the top
        window.print()  # Open the print dialog



def open_login_page():
    login_window = tk.Toplevel(root)
    login_window.title("Restaurant Software - Admin Login")
    maximize_window(login_window)

    center_frame = tk.Frame(login_window, bg="#f0f0f0", bd=5)
    center_frame.pack(expand=True, padx=20, pady=20)

    title_label = tk.Label(center_frame, text="Admin Login", font=("Arial", 24, "bold"), bg="#f0f0f0", fg="#333")
    title_label.pack(pady=10)

    user_label = tk.Label(center_frame, text="Username:", font=("Arial", 14), bg="#f0f0f0", fg="#333")
    user_label.pack()

    user_entry = tk.Entry(center_frame, font=("Arial", 12))
    user_entry.pack()

    pass_label = tk.Label(center_frame, text="Password:", font=("Arial", 14), bg="#f0f0f0", fg="#333")
    pass_label.pack()

    pass_entry = tk.Entry(center_frame, show="*", font=("Arial", 12))
    pass_entry.pack()

    def login_user():
        user_id = user_entry.get()
        password = pass_entry.get()

        cursor.execute('SELECT * FROM employees WHERE user_id = ? AND password = ?', (user_id, password))
        user = cursor.fetchone()

        if user:
            messagebox.showinfo("Login Successful", f"Welcome, {user_id}!")
            open_admin_dashboard()
            playsound('C:\\Users\\Gagan\\OneDrive\\Desktop\\canteen\\welcome.wav')

        else:
            messagebox.showerror("Login Failed", "Incorrect username or password")

    login_button = tk.Button(center_frame, text="Login", bg="#4CAF50", fg="white", font=("Arial", 14, "bold"), command=login_user)
    login_button.pack(pady=20, ipadx=10)

def open_add_user_page():
    add_user_window = tk.Toplevel(root)
    add_user_window.title("Add User")
    maximize_window(add_user_window)

    center_frame = tk.Frame(add_user_window, bg="#f0f0f0", bd=5)
    center_frame.pack(expand=True, padx=20, pady=20)

    title_label = tk.Label(center_frame, text="Add User", font=("Arial", 24, "bold"), bg="#f0f0f0", fg="#333")
    title_label.pack(pady=10)

    user_label = tk.Label(center_frame, text="Username:", font=("Arial", 14), bg="#f0f0f0", fg="#333")
    user_label.pack()

    user_entry = tk.Entry(center_frame, font=("Arial", 12))
    user_entry.pack()

    pass_label = tk.Label(center_frame, text="Password:", font=("Arial", 14), bg="#f0f0f0", fg="#333")
    pass_label.pack()

    pass_entry = tk.Entry(center_frame, show="*", font=("Arial", 12))
    pass_entry.pack()

    def add_user():
        user_id = user_entry.get()
        password = pass_entry.get()

        if not user_id or not password:
            messagebox.showerror("Error", "Please fill in all fields.")
        else:
            cursor.execute('SELECT * FROM employees WHERE user_id = ?', (user_id,))
            existing_user = cursor.fetchone()
            if existing_user:
                messagebox.showerror("Error", "User ID already exists. Please choose a different one.")
            else:
                cursor.execute('INSERT INTO employees (user_id, password) VALUES (?, ?)', (user_id, password))
                conn.commit()
                messagebox.showinfo("Success", f"User {user_id} added successfully!")

    add_user_button = tk.Button(center_frame, text="Add User", bg="#1E90FF", fg="white", font=("Arial", 14, "bold"), command=add_user)
    add_user_button.pack(pady=20, ipadx=10)

def open_delete_user_page():
    delete_user_window = tk.Toplevel(root)
    delete_user_window.title("Delete User")
    maximize_window(delete_user_window)

    center_frame = tk.Frame(delete_user_window, bg="#f0f0f0", bd=5)
    center_frame.pack(expand=True, padx=20, pady=20)

    title_label = tk.Label(center_frame, text="Delete User", font=("Arial", 24, "bold"), bg="#f0f0f0", fg="#333")
    title_label.pack(pady=10)

    user_label = tk.Label(center_frame, text="Username:", font=("Arial", 14), bg="#f0f0f0", fg="#333")
    user_label.pack()

    user_entry = tk.Entry(center_frame, font=("Arial", 12))
    user_entry.pack()

    pass_label = tk.Label(center_frame, text="Enter Password:", font=("Arial", 14), bg="#f0f0f0", fg="#333")
    pass_label.pack()

    pass_entry = tk.Entry(center_frame, show="*", font=("Arial", 12))
    pass_entry.pack()

    def delete_user():
        user_id = user_entry.get()
        password = pass_entry.get()

        if not user_id or not password:
            messagebox.showerror("Error", "Please fill in all fields.")
        else:
            cursor.execute('SELECT * FROM employees WHERE user_id = ? AND password = ?', (user_id, password))
            existing_user = cursor.fetchone()
            if existing_user:
                cursor.execute('DELETE FROM employees WHERE user_id = ?', (user_id,))
                conn.commit()
                messagebox.showinfo("Success", f"User {user_id} deleted successfully!")
            else:
                messagebox.showerror("Error", "Incorrect password or User ID not found.")

    delete_user_button = tk.Button(center_frame, text="Delete User", bg="#FF6347", fg="white", font=("Arial", 14, "bold"), command=delete_user)
    delete_user_button.pack(pady=20, ipadx=10)

def open_update_user_page():
    update_user_window = tk.Toplevel(root)
    update_user_window.title("Update User")
    maximize_window(update_user_window)

    center_frame = tk.Frame(update_user_window, bg="#f0f0f0", bd=5)
    center_frame.pack(expand=True, padx=20, pady=20)

    title_label = tk.Label(center_frame, text="Update User", font=("Arial", 24, "bold"), bg="#f0f0f0", fg="#333")
    title_label.pack(pady=10)

    user_label = tk.Label(center_frame, text="Username:", font=("Arial", 14), bg="#f0f0f0", fg="#333")
    user_label.pack()

    user_entry = tk.Entry(center_frame, font=("Arial", 12))
    user_entry.pack()

    old_pass_label = tk.Label(center_frame, text="Enter Old Password:", font=("Arial", 14), bg="#f0f0f0", fg="#333")
    old_pass_label.pack()

    old_pass_entry = tk.Entry(center_frame, show="*", font=("Arial", 12))
    old_pass_entry.pack()

    new_pass_label = tk.Label(center_frame, text="New Password:", font=("Arial", 14), bg="#f0f0f0", fg="#333")
    new_pass_label.pack()

    new_pass_entry = tk.Entry(center_frame, show="*", font=("Arial", 12))
    new_pass_entry.pack()

    def update_user():
        user_id = user_entry.get()
        old_password = old_pass_entry.get()
        new_password = new_pass_entry.get()

        if not user_id or not old_password or not new_password:
            messagebox.showerror("Error", "Please fill in all fields.")
        else:
            cursor.execute('SELECT * FROM employees WHERE user_id = ? AND password = ?', (user_id, old_password))
            existing_user = cursor.fetchone()
            if existing_user:
                cursor.execute('UPDATE employees SET password = ? WHERE user_id = ?', (new_password, user_id))
                conn.commit()
                messagebox.showinfo("Success", f"Password updated for user {user_id}!")
            else:
                messagebox.showerror("Error", "Incorrect old password or User ID not found.")

    update_user_button = tk.Button(center_frame, text="Update Password", bg="#1E90FF", fg="white", font=("Arial", 14, "bold"), command=update_user)
    update_user_button.pack(pady=20, ipadx=10)

# Main window
root = tk.Tk()
root.title("Restaurant Software")

center_frame = tk.Frame(root, bg="#f0f0f0", bd=5)
center_frame.pack(expand=True, padx=20, pady=20)

title_label = tk.Label(center_frame, text="Restaurant Software", font=("Arial", 24, "bold"), bg="#f0f0f0", fg="#333")
title_label.pack(pady=10)

login_button = tk.Button(center_frame, text="Admin Login", bg="#4CAF50", fg="white", font=("Arial", 14, "bold"), command=open_login_page)
login_button.pack(pady=20)

add_user_button = tk.Button(center_frame, text="Add User", bg="#1E90FF", fg="white", font=("Arial", 14, "bold"), command=open_add_user_page)
add_user_button.pack(pady=10)

delete_user_button = tk.Button(center_frame, text="Delete User", bg="#FF6347", fg="white", font=("Arial", 14, "bold"), command=open_delete_user_page)
delete_user_button.pack(pady=10)

update_user_button = tk.Button(center_frame, text="Update User", bg="#1E90FF", fg="white", font=("Arial", 14, "bold"), command=open_update_user_page)
update_user_button.pack(pady=10)

root.mainloop()
