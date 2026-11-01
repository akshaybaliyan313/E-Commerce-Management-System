import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

# ---------- Data (kept in memory) ----------
products = [
    {"name": "Wireless Mouse", "category": "Electronics", "price": 799.0, "stock": 25},
    {"name": "Bluetooth Speaker", "category": "Electronics", "price": 1999.0, "stock": 4},
    {"name": "Cotton T-Shirt", "category": "Clothing", "price": 499.0, "stock": 60},
    {"name": "Running Shoes", "category": "Footwear", "price": 2499.0, "stock": 0},
    {"name": "Notebook (Pack of 5)", "category": "Stationery", "price": 250.0, "stock": 100},
    {"name": "Water Bottle", "category": "Home", "price": 350.0, "stock": 3},
]


def get_status(stock):
    if stock == 0:
        return "Out of Stock"
    if stock <= 5:
        return "Low Stock"
    return "In Stock"


# ---------- Window ----------
root = tk.Tk()
root.title("E-Commerce Management System")
root.geometry("820x520")
root.configure(bg="#00bfff")

# Header
header = tk.Frame(root, bg="#1a1a2e")
header.pack(fill="x")
tk.Label(header, text="🛒  E-Commerce Management System", bg="#1a1a2e",
         fg="white", font=("Segoe UI", 14, "bold")).pack(side="left", padx=15, pady=10)
summary_label = tk.Label(header, bg="#1a1a2e", fg="#7fdbff", font=("Segoe UI", 9))
summary_label.pack(side="right", padx=15)

# Search + filter bar
bar = tk.Frame(root, bg="#00bfff")
bar.pack(fill="x", padx=15, pady=10)

tk.Label(bar, text="Search:", bg="#00bfff").pack(side="left")
search_var = tk.StringVar()
tk.Entry(bar, textvariable=search_var, width=28).pack(side="left", padx=5)

tk.Label(bar, text="Show:", bg="#00bfff").pack(side="left", padx=(15, 0))
filter_var = tk.StringVar(value="All")
filter_box = ttk.Combobox(bar, textvariable=filter_var, width=12, state="readonly",
                          values=["All", "In Stock", "Low Stock", "Out of Stock"])
filter_box.pack(side="left", padx=5)

# Table
table_frame = tk.Frame(root)
table_frame.pack(fill="both", expand=True, padx=15)

columns = ("Product", "Category", "Price", "Stock", "Status")
table = ttk.Treeview(table_frame, columns=columns, show="headings")
for col in columns:
    table.heading(col, text=col)
    table.column(col, anchor="center", width=140)
table.column("Product", anchor="w", width=220)

scroll = ttk.Scrollbar(table_frame, orient="vertical", command=table.yview)
table.configure(yscrollcommand=scroll.set)
table.pack(side="left", fill="both", expand=True)
scroll.pack(side="right", fill="y")

# Status line
status_label = tk.Label(root, bg="#00bfff", anchor="w", font=("Segoe UI", 8))
status_label.pack(fill="x", padx=15, pady=(5, 0))


# ---------- Functions ----------
def refresh(*args):
    """Reload the table based on search text and filter."""
    table.delete(*table.get_children())
    text = search_var.get().lower()
    shown = 0
    for i, p in enumerate(products):
        status = get_status(p["stock"])
        if text and text not in p["name"].lower() and text not in p["category"].lower():
            continue
        if filter_var.get() != "All" and filter_var.get() != status:
            continue
        table.insert("", "end", iid=str(i),
                     values=(p["name"], p["category"], f"₹{p['price']:.2f}", p["stock"], status))
        shown += 1
    status_label.config(text=f"Showing {shown} of {len(products)} products")
    total_value = sum(p["price"] * p["stock"] for p in products)
    summary_label.config(text=f"Inventory value: ₹{total_value:,.2f}")


def selected_index():
    sel = table.selection()
    if not sel:
        messagebox.showinfo("Select a product", "Please select a product first.")
        return None
    return int(sel[0])


def add_product():
    name = simpledialog.askstring("Add Product", "Product name:")
    if not name:
        return
    category = simpledialog.askstring("Add Product", "Category:") or "General"
    price = simpledialog.askfloat("Add Product", "Price:", minvalue=0)
    stock = simpledialog.askinteger("Add Product", "Stock quantity:", minvalue=0)
    if price is None or stock is None:
        return
    products.append({"name": name, "category": category, "price": price, "stock": stock})
    refresh()


def view_details():
    i = selected_index()
    if i is None:
        return
    p = products[i]
    messagebox.showinfo("Product Details",
                        f"Name: {p['name']}\nCategory: {p['category']}\n"
                        f"Price: ₹{p['price']:.2f}\nStock: {p['stock']}\n"
                        f"Status: {get_status(p['stock'])}")


def sell_product():
    i = selected_index()
    if i is None:
        return
    qty = simpledialog.askinteger("Sell", "Quantity to sell:", minvalue=1)
    if qty is None:
        return
    if qty > products[i]["stock"]:
        messagebox.showerror("Not enough stock", "Not enough items in stock.")
        return
    products[i]["stock"] -= qty
    total = qty * products[i]["price"]
    messagebox.showinfo("Sale complete", f"Sold {qty} item(s). Total: ₹{total:.2f}")
    refresh()


def restock_product():
    i = selected_index()
    if i is None:
        return
    qty = simpledialog.askinteger("Restock", "Quantity to add:", minvalue=1)
    if qty is None:
        return
    products[i]["stock"] += qty
    refresh()


def remove_product():
    i = selected_index()
    if i is None:
        return
    if messagebox.askyesno("Remove", f"Remove '{products[i]['name']}'?"):
        products.pop(i)
        refresh()


# ---------- Buttons ----------
tk.Button(bar, text="+ Add Product", bg="#0033ff", fg="white", relief="flat",
          command=add_product).pack(side="right")

btn_bar = tk.Frame(root, bg="#00bfff")
btn_bar.pack(fill="x", padx=15, pady=10)
for text, cmd in [("View Details", view_details), ("Sell", sell_product),
                  ("Restock", restock_product)]:
    tk.Button(btn_bar, text=text, width=12, command=cmd).pack(side="left", padx=(0, 8))
tk.Button(btn_bar, text="Remove", width=12, command=remove_product).pack(side="right")

# Live search / filter updates
search_var.trace_add("write", refresh)
filter_box.bind("<<ComboboxSelected>>", refresh)

refresh()
root.mainloop()
