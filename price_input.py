import tkinter as tk
from tkinter import messagebox
import mysql.connector
from database_setup import connect_to_database


def update_price(channel_id, price):
    try:
        connection = connect_to_database()
        cursor = connection.cursor()
        query = "UPDATE channels SET channel_price = %s WHERE channel_id = %s"
        cursor.execute(query, (price, channel_id))
        connection.commit()
        cursor.close()
        connection.close()
        return True
    except mysql.connector.Error as error:
        print("Error updating price:", error)
        return False

def submit_prices():
    for channel_id, price_var in channel_price_vars.items():
        price = price_var.get()
        if price.strip() != "":
            if not update_price(channel_id, price):
                messagebox.showerror("Error", f"Failed to update price for channel {channel_id}")
                return
    messagebox.showinfo("Success", "Prices updated successfully")

def main():
    global channel_price_vars

    root = tk.Tk()
    root.title("Channel Prices Input")

    # Fetch channel data from the database
    try:
        connection = connect_to_database()
        cursor = connection.cursor()
        cursor.execute("SELECT channel_id, channel_name, channel_price FROM channels")
        channels = cursor.fetchall()
        cursor.close()
        connection.close()
    except mysql.connector.Error as error:
        print("Error fetching channels:", error)
        messagebox.showerror("Error", "Failed to fetch channels from database")
        return

    channel_price_vars = {}

    # Create labels and entry fields for each channel
    for idx, (channel_id, channel_name, channel_price) in enumerate(channels):
        label = tk.Label(root, text=f"{channel_name} ({channel_id}):")
        label.grid(row=idx, column=0, padx=5, pady=5, sticky="w")
        price_var = tk.StringVar()
        price_var.set(channel_price)
        entry = tk.Entry(root, textvariable=price_var)
        entry.grid(row=idx, column=1, padx=5, pady=5, sticky="w")
        channel_price_vars[channel_id] = price_var

    # Create submit button
    submit_button = tk.Button(root, text="Submit", command=submit_prices)
    submit_button.grid(row=len(channels), column=0, columnspan=2, pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()
