import customtkinter as ctk
from tkinter import messagebox
import os
import csv
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

login_attempts = 0
current_user_role = None
records = []



def load_users():
    users = []

    users_path = os.path.join(os.path.dirname(__file__), "users.csv")

    try:
        with open(users_path, "r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file, delimiter=";")
            users = list(reader)

    except FileNotFoundError:
        print("users.csv not found!")

    return users

def load_records():
    global records

    import os

    csv_path = os.path.join(os.path.dirname(__file__), "records.csv")

    print("Loading:", csv_path)
    print("Exists:", os.path.exists(csv_path))

    try:
        with open(csv_path, "r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file, delimiter=";")
            records = list(reader)

        # Convert numeric fields
        for r in records:
            r["layers"] = int(r["layers"])
            r["eggs_produced"] = int(r["eggs_produced"])
            r["feed_used"] = float(r["feed_used"])
            r["feed_price"] = float(r["feed_price"])
            r["feed_cost"] = float(r["feed_cost"])
            r["eggs_sold"] = int(r["eggs_sold"])
            r["price_per_egg"] = float(r["price_per_egg"])
            r["revenue"] = float(r["revenue"])

        print("Loaded", len(records), "records.")

    except Exception as e:
        print("Error loading records:", e)
        records = []

def display_users_gui():
    users = load_users()

    users_text = ""

    for user in users:
        users_text += f"{user['username']} - {user['role']}\n"

    users_display_label.configure(text=users_text)
    
    
def display_users():
    users = load_users()

    users_text = "===== SYSTEM USERS =====\n\n"

    for user in users:
        users_text += f"{user['username']} - {user['role']}\n"

    users_display_label.configure(text=users_text)
    
    

def login():
    global login_attempts
    global current_user_role

    users = load_users()
    max_attempts = 3

    username = username_entry.get()
    password = password_entry.get()

    for user in users:
        if username == user["username"] and password == user["password"]:

            messagebox.showinfo(
                "Login Successful",
                f"Welcome {username}!\nRole: {user['role']}"
)
            user_info_label.configure(
                text=f"Welcome, {username}!\nRole: {user['role']}"
)
            role = user["role"]
            current_user_role = role
         
            user_management_button.pack_forget()

            if current_user_role in ["Administrator", "Manager"]:
                user_management_button.pack(pady=10)
    
            add_user_button.pack_forget()

            if current_user_role == "Administrator":
                add_user_button.pack(pady=10)
    
            delete_user_button.pack_forget()

            if current_user_role == "Administrator":
                delete_user_button.pack(pady=10)
    
            login_frame.pack_forget()
            dashboard_frame.pack(fill="both", expand=True)

            return user

    login_attempts += 1

    remaining = max_attempts - login_attempts

    if remaining > 0:
        messagebox.showerror(
        "Login Failed",
        f"Invalid username or password.\n"
        f"Attempts remaining: {remaining}"
    )

        password_entry.delete(0, "end")
        password_entry.focus()
    else:
       messagebox.showerror(
        "Login Failed",
        "Too many failed login attempts."
    )

       login_button.configure(state="disabled")

    return None


def start_system():
    welcome_frame.pack_forget()
    login_frame.pack(fill="both", expand=True)


# Create the main window
app = ctk.CTk()

# Window title
app.title("Smart Egg Production System v2.0")

# Window size
app.geometry("800x500")
# Create the welcome frame
welcome_frame = ctk.CTkFrame(app)

welcome_frame.pack(fill="both", expand=True)


welcome_label = ctk.CTkLabel(welcome_frame,
    text="Welcome to Smart Egg Production System",
    font=("Arial", 24, "bold")
)

# Create the login frame
login_frame = ctk.CTkFrame(app)
# Login title
login_label = ctk.CTkLabel(
    login_frame,
    text="User Login",
    font=("Arial", 24, "bold")
)

login_label.pack(pady=20)

username_entry = ctk.CTkEntry(
    login_frame,
    placeholder_text="Username",
    width=250
)

username_entry.pack(pady=10)


password_entry = ctk.CTkEntry(
    login_frame,
    placeholder_text="Password",
    show="*",
    width=250
)

password_entry.pack(pady=10)

login_button = ctk.CTkButton(
    login_frame,
    text="Login",
    command=login
)

login_button.pack(pady=20)

welcome_label.pack(pady=40)

start_button = ctk.CTkButton(welcome_frame,
    text="Start System",
    command=start_system
)


start_button.pack(pady=20)

# Load farm records before creating the dashboard
load_records()

# Dashboard frame

dashboard_frame = ctk.CTkScrollableFrame(
    app
)

# KPI Cards Frame
kpi_frame = ctk.CTkFrame(dashboard_frame)
kpi_frame.pack(pady=20)

# -----------------------------
# Total Eggs Produced
# -----------------------------

total_eggs_card = ctk.CTkFrame(
    kpi_frame,
    width=220,
    height=120
)

total_eggs_card.grid(row=0, column=0, padx=15, pady=15)

total_eggs_title = ctk.CTkLabel(
    total_eggs_card,
    text="Total Eggs Produced",
    font=("Arial", 16, "bold")
)

total_eggs_title.pack(pady=(15, 5))

total_eggs_value = ctk.CTkLabel(
    total_eggs_card,
    text=str(sum(r["eggs_produced"] for r in records)),
    font=("Arial", 24, "bold")
)

total_eggs_value.pack(pady=5)


# -----------------------------
# Total Eggs Sold
# -----------------------------

total_eggs_sold_card = ctk.CTkFrame(
    kpi_frame,
    width=220,
    height=120
)

total_eggs_sold_card.grid(row=0, column=1, padx=15, pady=15)

total_eggs_sold_title = ctk.CTkLabel(
    total_eggs_sold_card,
    text="Total Eggs Sold",
    font=("Arial", 16, "bold")
)

total_eggs_sold_title.pack(pady=(15, 5))

total_eggs_sold_value = ctk.CTkLabel(
    total_eggs_sold_card,
    text=str(sum(r["eggs_sold"] for r in records)),
    font=("Arial", 24, "bold")
)

total_eggs_sold_value.pack(pady=5)


# -----------------------------
# Total Revenue
# -----------------------------

total_revenue_card = ctk.CTkFrame(
    kpi_frame,
    width=220,
    height=120
)

total_revenue_card.grid(row=1, column=0, padx=15, pady=15)

total_revenue_title = ctk.CTkLabel(
    total_revenue_card,
    text="Total Revenue",
    font=("Arial", 16, "bold")
)

total_revenue_title.pack(pady=(15, 5))

total_revenue_value = ctk.CTkLabel(
    total_revenue_card,
    text=f"R{sum(r['revenue'] for r in records):,.2f}",
    font=("Arial", 24, "bold")
)

total_revenue_value.pack(pady=5)


# -----------------------------
# Total Feed Cost
# -----------------------------

total_feed_cost_card = ctk.CTkFrame(
    kpi_frame,
    width=220,
    height=120
)

total_feed_cost_card.grid(row=1, column=1, padx=15, pady=15)

total_feed_cost_title = ctk.CTkLabel(
    total_feed_cost_card,
    text="Total Feed Cost",
    font=("Arial", 16, "bold")
)

total_feed_cost_title.pack(pady=(15, 5))

total_feed_cost_value = ctk.CTkLabel(
    total_feed_cost_card,
    text=f"R{sum(r['feed_cost'] for r in records):,.2f}",
    font=("Arial", 24, "bold")
)

total_feed_cost_value.pack(pady=5)


# -----------------------------
# Total Profit
# -----------------------------

total_profit_card = ctk.CTkFrame(
    kpi_frame,
    width=220,
    height=120
)

total_profit_card.grid(row=1, column=2, padx=15, pady=15)

total_profit_title = ctk.CTkLabel(
    total_profit_card,
    text="Total Profit",
    font=("Arial", 16, "bold")
)

total_profit_title.pack(pady=(15, 5))

total_profit_value = ctk.CTkLabel(
    total_profit_card,
    text=f"R{sum(r['revenue'] for r in records) - sum(r['feed_cost'] for r in records):,.2f}",
    font=("Arial", 24, "bold")
)

total_profit_value.pack(pady=5)
dashboard_label = ctk.CTkLabel(
    dashboard_frame,
    text="Dashboard",
    font=("Arial", 28, "bold")
)

# -----------------------------
# Production Efficiency
# -----------------------------

total_layers = sum(r["layers"] for r in records)
total_eggs = sum(r["eggs_produced"] for r in records)

if total_layers > 0:
    production_efficiency = (total_eggs / total_layers) * 100
else:
    production_efficiency = 0

production_efficiency_card = ctk.CTkFrame(
    kpi_frame,
    width=220,
    height=120
)

production_efficiency_card.grid(
    row=0,
    column=2,
    padx=15,
    pady=15
)

production_efficiency_title = ctk.CTkLabel(
    production_efficiency_card,
    text="Production Efficiency",
    font=("Arial", 16, "bold")
)

production_efficiency_title.pack(pady=(15, 5))

production_efficiency_value = ctk.CTkLabel(
    production_efficiency_card,
    text=f"{production_efficiency:.2f}%",
    font=("Arial", 24, "bold")
)

production_efficiency_value.pack(pady=5)

# -----------------------------
# Production Analysis
# -----------------------------

production_chart_frame = ctk.CTkFrame(
    dashboard_frame
)

production_chart_frame.pack(
    fill="x",
    padx=20,
    pady=20
)

production_chart_title = ctk.CTkLabel(
    production_chart_frame,
    text="Egg Production Trend",
    font=("Arial", 22, "bold")
)

production_chart_title.pack(pady=15)


# Prepare production data
dates = [r["date"] for r in records]
eggs_produced = [r["eggs_produced"] for r in records]


# Create chart
figure, ax = plt.subplots(
    figsize=(10, 4)
)

ax.plot(
    dates,
    eggs_produced,
    marker="o"
)

ax.set_title("Egg Production Trend")
ax.set_xlabel("Date")
ax.set_ylabel("Eggs Produced")

ax.tick_params(
    axis="x",
    rotation=45
)

figure.tight_layout()


# Display chart inside CustomTkinter
chart_canvas = FigureCanvasTkAgg(
    figure,
    master=production_chart_frame
)

chart_canvas.draw()

chart_canvas.get_tk_widget().pack(
    fill="both",
    expand=True,
    padx=15,
    pady=15
)

# -----------------------------
# Best Production Day
# -----------------------------

if records:
    best_production_record = max(
        records,
        key=lambda r: r["eggs_produced"]
    )

    best_production_date = best_production_record["date"]
    best_production_eggs = best_production_record["eggs_produced"]
else:
    best_production_date = "No data"
    best_production_eggs = 0


best_production_frame = ctk.CTkFrame(
    dashboard_frame
)

best_production_frame.pack(
    fill="x",
    padx=20,
    pady=10
)

best_production_title = ctk.CTkLabel(
    best_production_frame,
    text="Best Production Day",
    font=("Arial", 20, "bold")
)

best_production_title.pack(pady=(15, 5))

best_production_value = ctk.CTkLabel(
    best_production_frame,
    text=f"{best_production_date}\n{best_production_eggs:,} eggs produced",
    font=("Arial", 18)
)

best_production_value.pack(pady=(5, 15))


# -----------------------------
# Production Analysis# -----------------------------
# Worst Production Day
# -----------------------------

if records:
    worst_production_record = min(
        records,
        key=lambda r: r["eggs_produced"]
    )

    worst_production_date = worst_production_record["date"]
    worst_production_eggs = worst_production_record["eggs_produced"]
else:
    worst_production_date = "No data"
    worst_production_eggs = 0


worst_production_frame = ctk.CTkFrame(
    dashboard_frame
)

worst_production_frame.pack(
    fill="x",
    padx=20,
    pady=10
)

worst_production_title = ctk.CTkLabel(
    worst_production_frame,
    text="Worst Production Day",
    font=("Arial", 20, "bold")
)

worst_production_title.pack(pady=(15, 5))

worst_production_value = ctk.CTkLabel(
    worst_production_frame,
    text=f"{worst_production_date}\n{worst_production_eggs:,} eggs produced",
    font=("Arial", 18)
)

worst_production_value.pack(pady=(5, 15))

# -----------------------------
# Average Eggs Per Day
# -----------------------------

if records:
    total_eggs_produced = sum(
        r["eggs_produced"] for r in records
    )

    average_eggs_per_day = (
        total_eggs_produced / len(records)
    )
else:
    average_eggs_per_day = 0


average_eggs_frame = ctk.CTkFrame(
    dashboard_frame
)

average_eggs_frame.pack(
    fill="x",
    padx=20,
    pady=10
)

average_eggs_title = ctk.CTkLabel(
    average_eggs_frame,
    text="Average Eggs Per Day",
    font=("Arial", 20, "bold")
)

average_eggs_title.pack(pady=(15, 5))

average_eggs_value = ctk.CTkLabel(
    average_eggs_frame,
    text=f"{average_eggs_per_day:,.2f} eggs",
    font=("Arial", 18)
)

average_eggs_value.pack(pady=(5, 15))

# -----------------------------
# Monthly Egg Production
# -----------------------------

from collections import defaultdict
from datetime import datetime

monthly_eggs = defaultdict(int)

for record in records:
    try:
        date = datetime.strptime(record["date"], "%Y-%m-%d")
        month = date.strftime("%B %Y")
        monthly_eggs[month] += record["eggs_produced"]
    except ValueError:
        continue


monthly_eggs_frame = ctk.CTkFrame(
    dashboard_frame
)

monthly_eggs_frame.pack(
    fill="x",
    padx=20,
    pady=10
)

monthly_eggs_title = ctk.CTkLabel(
    monthly_eggs_frame,
    text="Monthly Egg Production",
    font=("Arial", 20, "bold")
)

monthly_eggs_title.pack(pady=(15, 10))


for month, total in monthly_eggs.items():

    monthly_label = ctk.CTkLabel(
        monthly_eggs_frame,
        text=f"{month}: {total:,} eggs",
        font=("Arial", 16)
    )

    monthly_label.pack(pady=3)
    
    # -----------------------------
# Feed Efficiency
# -----------------------------

total_eggs_produced = sum(
    r["eggs_produced"] for r in records
)

total_feed_used = sum(
    r["feed_used"] for r in records
)

if total_feed_used > 0:
    feed_efficiency = (
        total_eggs_produced / total_feed_used
    )
else:
    feed_efficiency = 0


feed_efficiency_frame = ctk.CTkFrame(
    dashboard_frame
)

feed_efficiency_frame.pack(
    fill="x",
    padx=20,
    pady=10
)

feed_efficiency_title = ctk.CTkLabel(
    feed_efficiency_frame,
    text="Feed Efficiency",
    font=("Arial", 20, "bold")
)

feed_efficiency_title.pack(pady=(15, 5))

feed_efficiency_value = ctk.CTkLabel(
    feed_efficiency_frame,
    text=f"{feed_efficiency:.2f} eggs/kg",
    font=("Arial", 18)
)

feed_efficiency_value.pack(pady=(5, 15))

# -----------------------------
# Farm Management
# -----------------------------

farm_management_frame = ctk.CTkFrame(
    dashboard_frame
)

farm_management_frame.pack(
    fill="x",
    padx=20,
    pady=20
)

farm_management_title = ctk.CTkLabel(
    farm_management_frame,
    text="Farm Management",
    font=("Arial", 22, "bold")
)

farm_management_title.pack(pady=(15, 10))

# -----------------------------
# Add Farm Record Frame
# -----------------------------

def save_record_gui():
    try:
        # Get values from the GUI
        date = date_entry.get().strip()
        layers = int(layers_entry.get())
        eggs_produced = int(eggs_produced_entry.get())
        feed_used = float(feed_used_entry.get())
        feed_price = float(feed_price_entry.get())
        eggs_sold = int(eggs_sold_entry.get())
        price_per_egg = float(price_per_egg_entry.get())
        notes = notes_entry.get().strip()

        # Check date
        if not date:
            messagebox.showerror(
                "Invalid Input",
                "Please enter a date."
            )
            return

        # Check duplicate date
        for record in records:
            if record["date"] == date:
                messagebox.showerror(
                    "Duplicate Record",
                    "A record for this date already exists."
                )
                return

        # Validation
        if layers <= 0:
            messagebox.showerror(
                "Invalid Input",
                "Number of layers must be greater than 0."
            )
            return

        if eggs_produced < 0 or eggs_sold < 0:
            messagebox.showerror(
                "Invalid Input",
                "Egg quantities cannot be negative."
            )
            return

        if feed_used < 0 or feed_price < 0 or price_per_egg < 0:
            messagebox.showerror(
                "Invalid Input",
                "Feed and price values cannot be negative."
            )
            return

        if eggs_sold > eggs_produced:
            messagebox.showerror(
                "Invalid Input",
                "Eggs sold cannot exceed eggs produced."
            )
            return

        # Same calculations as Version 1
        feed_cost = feed_used * feed_price
        revenue = eggs_sold * price_per_egg
        production_rate = calculate_production_rate(
            layers,
            eggs_produced
        )

        # Create record
        record = {
            "date": date,
            "layers": layers,
            "eggs_produced": eggs_produced,
            "feed_used": feed_used,
            "feed_price": feed_price,
            "feed_cost": feed_cost,
            "eggs_sold": eggs_sold,
            "price_per_egg": price_per_egg,
            "revenue": revenue,
            "notes": notes
        }

        # Add to existing records list
        records.append(record)

        # Save to the existing records.csv
        save_records()
        
        messagebox.showinfo(
            "Record Saved",
            f"Farm record saved successfully!\n\n"
            f"Revenue: R{revenue:,.2f}\n"
            f"Feed Cost: R{feed_cost:,.2f}\n"
            f"Production Rate: {production_rate:.2f}%"
        )

        # Clear the form
        date_entry.delete(0, "end")
        layers_entry.delete(0, "end")
        eggs_produced_entry.delete(0, "end")
        feed_used_entry.delete(0, "end")
        feed_price_entry.delete(0, "end")
        eggs_sold_entry.delete(0, "end")
        price_per_egg_entry.delete(0, "end")
        notes_entry.delete(0, "end")

        # Return to dashboard
        add_record_frame.pack_forget()
        dashboard_frame.pack(fill="both", expand=True)

    except ValueError:
        messagebox.showerror(
            "Invalid Input",
            "Please enter valid numbers in the numeric fields."
        )

add_record_frame = ctk.CTkScrollableFrame(app)

add_record_title = ctk.CTkLabel(
    add_record_frame,
    text="Add Farm Record",
    font=("Arial", 24, "bold")
)

form_frame = ctk.CTkFrame(
    add_record_frame
)

form_frame.pack(
    padx=20,
    pady=10
)

form_frame.grid_columnconfigure(0, weight=1)
form_frame.grid_columnconfigure(1, weight=1)

# -----------------------------
# Add Farm Record Form Fields
# -----------------------------

# Date
date_label = ctk.CTkLabel(
    form_frame,
    text="Date (YYYY-MM-DD)"
)

date_label.grid(
    row=0,
    column=0,
    padx=15,
    pady=(10, 2),
    sticky="w"
)

date_entry = ctk.CTkEntry(
    form_frame,
    width=250,
    placeholder_text="YYYY-MM-DD"
)

date_entry.grid(
    row=1,
    column=0,
    padx=15,
    pady=(0, 10)
)


# Number of Layers
layers_label = ctk.CTkLabel(
    form_frame,
    text="Number of Layers"
)

layers_label.grid(
    row=0,
    column=1,
    padx=15,
    pady=(10, 2),
    sticky="w"
)

layers_entry = ctk.CTkEntry(
    form_frame,
    width=250,
    placeholder_text="Enter number of layers"
)

layers_entry.grid(
    row=1,
    column=1,
    padx=15,
    pady=(0, 10)
)


# Eggs Produced
eggs_produced_label = ctk.CTkLabel(
    form_frame,
    text="Eggs Produced"
)

eggs_produced_label.grid(
    row=2,
    column=0,
    padx=15,
    pady=(10, 2),
    sticky="w"
)

eggs_produced_entry = ctk.CTkEntry(
    form_frame,
    width=250,
    placeholder_text="Enter eggs produced"
)

eggs_produced_entry.grid(
    row=3,
    column=0,
    padx=15,
    pady=(0, 10)
)


# Feed Used
feed_used_label = ctk.CTkLabel(
    form_frame,
    text="Feed Used (kg)"
)

feed_used_label.grid(
    row=2,
    column=1,
    padx=15,
    pady=(10, 2),
    sticky="w"
)

feed_used_entry = ctk.CTkEntry(
    form_frame,
    width=250,
    placeholder_text="Enter feed used in kg"
)

feed_used_entry.grid(
    row=3,
    column=1,
    padx=15,
    pady=(0, 10)
)


# Feed Price
feed_price_label = ctk.CTkLabel(
    form_frame,
    text="Feed Price per kg (R)"
)

feed_price_label.grid(
    row=4,
    column=0,
    padx=15,
    pady=(10, 2),
    sticky="w"
)

feed_price_entry = ctk.CTkEntry(
    form_frame,
    width=250,
    placeholder_text="Enter feed price per kg"
)

feed_price_entry.grid(
    row=5,
    column=0,
    padx=15,
    pady=(0, 10)
)


# Eggs Sold
eggs_sold_label = ctk.CTkLabel(
    form_frame,
    text="Eggs Sold"
)

eggs_sold_label.grid(
    row=4,
    column=1,
    padx=15,
    pady=(10, 2),
    sticky="w"
)

eggs_sold_entry = ctk.CTkEntry(
    form_frame,
    width=250,
    placeholder_text="Enter eggs sold"
)

eggs_sold_entry.grid(
    row=5,
    column=1,
    padx=15,
    pady=(0, 10)
)


# Price per Egg
price_per_egg_label = ctk.CTkLabel(
    form_frame,
    text="Price per Egg (R)"
)

price_per_egg_label.grid(
    row=6,
    column=0,
    padx=15,
    pady=(10, 2),
    sticky="w"
)

price_per_egg_entry = ctk.CTkEntry(
    form_frame,
    width=250,
    placeholder_text="Enter price per egg"
)

price_per_egg_entry.grid(
    row=7,
    column=0,
    padx=15,
    pady=(0, 10)
)


# Notes
notes_label = ctk.CTkLabel(
    form_frame,
    text="Notes (Optional)"
)

notes_label.grid(
    row=6,
    column=1,
    padx=15,
    pady=(10, 2),
    sticky="w"
)

notes_entry = ctk.CTkEntry(
    form_frame,
    width=250,
    placeholder_text="Enter notes"
)

notes_entry.grid(
    row=7,
    column=1,
    padx=15,
    pady=(0, 10)
)

save_record_button = ctk.CTkButton(
    add_record_frame,
    text="Save Record",
    command=save_record_gui,
    width=250,
    height=40
)

save_record_button.pack(
    pady=20
)

add_record_button = ctk.CTkButton(
    farm_management_frame,
    text="Add Farm Record",
    command=lambda: (
        dashboard_frame.pack_forget(),
        add_record_frame.pack(fill="both", expand=True)
    )
)

add_record_button.pack(
    pady=10
)
# -----------------------------

production_chart_frame = ctk.CTkFrame(
    dashboard_frame
)

production_chart_frame.pack(
    fill="both",
    expand=True,
    padx=20,
    pady=20
)

production_chart_title = ctk.CTkLabel(
    production_chart_frame,
    text="Egg Production Trend",
    font=("Arial", 22, "bold")
)

production_chart_title.pack(pady=15)

dashboard_label.pack(pady=40)
user_info_label = ctk.CTkLabel(
    dashboard_frame,
    text="",
    font=("Arial", 18)
)

user_info_label.pack(pady=10)

user_management_button = ctk.CTkButton(
    dashboard_frame,
    text="User Management",
    command=lambda: (
        dashboard_frame.pack_forget(),
        user_management_frame.pack(fill="both", expand=True)
    )
)



# View Users frame
view_users_frame = ctk.CTkFrame(app)

view_users_label = ctk.CTkLabel(
    view_users_frame,
    text="System Users",
    font=("Arial", 24, "bold")
)

view_users_label.pack(pady=20)

users_display_label = ctk.CTkLabel(
    view_users_frame,
    text="",
    font=("Arial", 16)
)

users_display_label.pack(pady=20)

def delete_user_gui():
    username = delete_username_entry.get()

    if username == "":
        messagebox.showerror("Error", "Please enter a username.")
        return

    with open("users.csv", "r") as file:
        lines = file.readlines()

    user_found = False

    for line in lines:
        existing_username = line.strip().split(";")[0]

        if existing_username == username:
            user_found = True
            break

    if not user_found:
        messagebox.showerror("Error", "Username not found.")
        return

    confirm = messagebox.askyesno(
        "Confirm Delete",
        f"Are you sure you want to delete '{username}'?"
    )

    if not confirm:
        return

    with open("users.csv", "w") as file:
        for line in lines:
            existing_username = line.strip().split(";")[0]

            if existing_username != username:
                file.write(line)

    messagebox.showinfo(
        "Success",
        "User deleted successfully!"
    )

    delete_username_entry.delete(0, "end")
    display_users_gui()
    
delete_username_entry = ctk.CTkEntry(
    view_users_frame,
    placeholder_text="Enter username to delete",
    width=250
)

delete_username_entry.pack(pady=10)

delete_user_button = ctk.CTkButton(
    view_users_frame,
    text="Delete User",
    command=delete_user_gui
)


# User Management frame
user_management_frame = ctk.CTkFrame(app)

user_management_label = ctk.CTkLabel(
    user_management_frame,
    text="User Management",
    font=("Arial", 28, "bold")
)

user_management_label.pack(pady=40)

view_users_button = ctk.CTkButton(
    user_management_frame,
    text="View Users",
    command=lambda: (
    user_management_frame.pack_forget(),
    view_users_frame.pack(fill="both", expand=True),
    display_users_gui()
)
)



view_users_button.pack(pady=10)

add_user_button = ctk.CTkButton(
    user_management_frame,
    text="Add User",
    command=lambda: (
        user_management_frame.pack_forget(),
        add_user_frame.pack(fill="both", expand=True)
    )
)


back_user_management_button = ctk.CTkButton(
    user_management_frame,
    text="Back",
    command=lambda: (
        user_management_frame.pack_forget(),
        dashboard_frame.pack(fill="both", expand=True)
    )
)

back_user_management_button.pack(pady=10)


# Add User frame
def save_new_user():
    username = add_username_entry.get()
    password = add_password_entry.get()
    role = role_dropdown.get()

    if username == "":
        print("Please enter a username.")
        return

    if password == "":
        print("Please enter a password.")
        return
    
    with open("users.csv", "r") as file:
       for line in file:
        existing_username = line.strip().split(";")[0]

        if existing_username == username:
            print("Username already exists.")
            return

    with open("users.csv", "a") as file:
        file.write(f"{username};{password};{role}\n")

    messagebox.showinfo(
    "Success",
    "User saved successfully!"
)
    
    add_username_entry.delete(0, "end")
    add_password_entry.delete(0, "end")
    role_dropdown.set("Employee")
    
    display_users_gui()
    
add_user_frame = ctk.CTkFrame(app)

add_user_label = ctk.CTkLabel(
    add_user_frame,
    text="Add User",
    font=("Arial", 28, "bold")
)

add_user_label.pack(pady=30)

username_label = ctk.CTkLabel(
    add_user_frame,
    text="Username"
)

username_label.pack(pady=5)

add_username_entry = ctk.CTkEntry(
    add_user_frame,
    placeholder_text="Enter username",
    width=250
)

add_username_entry.pack(pady=5)

password_label = ctk.CTkLabel(
    add_user_frame,
    text="Password"
)

password_label.pack(pady=5)


add_password_entry = ctk.CTkEntry(
    add_user_frame,
    placeholder_text="Enter password",
    show="*",
    width=250
)

add_password_entry.pack(pady=5)

role_label = ctk.CTkLabel(
    add_user_frame,
    text="Select Role"
)

role_label.pack(pady=5)

role_dropdown = ctk.CTkComboBox(
    add_user_frame,
    values=["Administrator", "Manager", "Employee"],
    width=250
)

role_dropdown.pack(pady=5)
role_dropdown.set("Employee")

back_add_user_button = ctk.CTkButton(
    add_user_frame,
    text="Back to User Management",
    command=lambda: (
        add_user_frame.pack_forget(),
        user_management_frame.pack(fill="both", expand=True)
    )
)

back_add_user_button.pack(pady=10)

save_user_button = ctk.CTkButton(
    add_user_frame,
    text="Save User",
    command=save_new_user
)

save_user_button.pack(pady=20)

# View Users frame
view_users_frame = ctk.CTkFrame(app)

view_users_label = ctk.CTkLabel(
    view_users_frame,
    text="System Users",
    font=("Arial", 24, "bold")
)

view_users_label.pack(pady=20)

users_display_label = ctk.CTkLabel(
    view_users_frame,
    text="",
    font=("Arial", 16)
)

users_display_label.pack(pady=20)

delete_username_entry = ctk.CTkEntry(
    view_users_frame,
    placeholder_text="Enter username to delete",
    width=250
)

delete_username_entry.pack(pady=10)

delete_user_button = ctk.CTkButton(
    view_users_frame,
    text="Delete User",
    command=delete_user_gui
)

delete_user_button.pack(pady=10)

back_users_button = ctk.CTkButton(
    view_users_frame,
    text="Back to User Management",
    command=lambda: (
        view_users_frame.pack_forget(),
        user_management_frame.pack(fill="both", expand=True)
    )
)

back_users_button.pack(pady=20)



# Keep the window open
app.mainloop()
