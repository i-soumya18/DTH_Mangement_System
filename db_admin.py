from tkinter import Tk, Label, Entry, Button, messagebox, END
from database_setup import get_profile_data, delete_user

def show_user_details():
    email = email_entry.get()
    user = get_profile_data(email)
    if user:
        # Display user details
        name_label.config(text="Name: " + user[1])
        phone_label.config(text="Phone Number: " + user[3])
        street_label.config(text="Street: " + user[4])
        state_label.config(text="State: " + user[5])
        city_label.config(text="City: " + user[6])
        zip_code_label.config(text="Zip Code: " + user[7])
    else:
        messagebox.showinfo("Error", "User not found")

# Function to delete user based on email
def delete_user_handler():
    email = email_entry.get()
    if email:
        confirm = messagebox.askyesno("Confirm", f"Are you sure you want to delete user with email: {email}?")
        if confirm:
            delete_user(email)
            messagebox.showinfo("Success", f"User with email {email} deleted successfully.")
            email_entry.delete(0, 'end')  # Use 'end' instead of END
    else:
        messagebox.showwarning("Warning", "Please enter the email of the user to delete.")

# Create GUI window
root = Tk()
root.title("Admin Panel")

# Email entry
email_label = Label(root, text="Enter Email:")
email_label.grid(row=0, column=0)
email_entry = Entry(root)
email_entry.grid(row=0, column=1)

# Buttons
show_button = Button(root, text="Show Details", command=show_user_details)
show_button.grid(row=1, column=0)
delete_button = Button(root, text="Delete User", command=delete_user_handler)
delete_button.grid(row=1, column=1)

# Labels to display user details
name_label = Label(root, text="")
name_label.grid(row=2, column=0, columnspan=2)
phone_label = Label(root, text="")
phone_label.grid(row=3, column=0, columnspan=2)
street_label = Label(root, text="")
street_label.grid(row=4, column=0, columnspan=2)
state_label = Label(root, text="")
state_label.grid(row=5, column=0, columnspan=2)
city_label = Label(root, text="")
city_label.grid(row=6, column=0, columnspan=2)
zip_code_label = Label(root, text="")
zip_code_label.grid(row=7, column=0, columnspan=2)

root.mainloop()
