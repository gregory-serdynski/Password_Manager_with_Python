from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import random
import json
import pyperclip

LETTERS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
           'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
           'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
NUMBERS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
SYMBOLS = ['!', '#', '$', '%', '&', '(', ')', '*', '+']
BLUE = "#24a0ed"
data_result = ""
conf_win = None
war_win = None


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    rand_letter_num = random.randint(5, 7)
    rand_number_num = random.randint(5, 7)
    rand_symbol_num = random.randint(5, 7)

    password_letters = [random.choice(LETTERS) for _ in range(rand_letter_num)]
    password_numbers = [random.choice(NUMBERS) for _ in range(rand_number_num)]
    password_symbols = [random.choice(SYMBOLS) for _ in range(rand_symbol_num)]

    password_list = password_letters + password_numbers + password_symbols

    random.shuffle(password_list)
    password = "".join(password_list)
    password_entry.delete(0, END)
    password_entry.insert(0, password)

    # Copy to clipboard - two methods
    window.clipboard_clear()
    window.clipboard_append(password)
    # pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #

def save_data():
    global data_result
    website_data = website_entry.get()
    email_data = username_entry.get()
    password_data = password_entry.get()
    new_data = {
        website_data: {
            "email": email_data,
            "password": password_data
        }
    }

    if website_data == "" or email_data == "" or password_data == "":
        messagebox.showinfo("Oops", "Please don't leave any fields empty!")
    else:
        try:
            with open(file="data.json", mode="r") as json_file:
                data = json.load(json_file)
        except FileNotFoundError:
            with open(file="data.json", mode="w") as json_file:
                json.dump(new_data, json_file, indent=4)
        else:
            data.update(new_data)
            print(data)
            with open(file="data.json", mode="w") as json_file:
                json.dump(data, json_file, indent=4)
        finally:
            messagebox.showinfo("Saving complete", "Data was added")


# ---------------------------- Search ------------------------------ #

def find_password():
    web_data = website_entry.get()
    try:
        with open(file="data.json", mode="r") as data_file:
            data = json.load(data_file)
            email_info = data[web_data]["email"]
            password_info = data[web_data]["password"]
    except FileNotFoundError:
        messagebox.showinfo("Error", "No data found.")
    except KeyError:
        messagebox.showinfo("Error", "No data found.")
    else:
        messagebox.showinfo(f"{web_data}", f"Email: {email_info}\nPassword: {password_info}")


# ---------------------------- Reset ------------------------------- #

def reset_data():
    website_entry.delete(0, END)
    # username_entry.delete(0, END)
    password_entry.delete(0, END)
    website_entry.focus()


# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Password Manager")
window.config(pady=30, padx=30)

style = ttk.Style()
style.configure('TButton', width=20, borderwidth=1, focusthickness=3, focuscolor='none')
style.map('TButton', background=[('active', BLUE)])

# Canvas
canvas = Canvas(width=200, height=200)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(column=1, row=0, columnspan=2)

# Labels
website_label = ttk.Label(text="Website:")
website_label.grid(column=0, row=1, pady=3)

username_label = ttk.Label(text="Email/Username:")
username_label.grid(column=0, row=2)

password_label = ttk.Label(text="Password:")
password_label.grid(column=0, row=3, pady=3)

# Entries
website_entry = ttk.Entry(width=25)
website_entry.focus()
website_entry.grid(column=1, row=1)

username_entry = ttk.Entry(width=50)
username_entry.insert(0, 'serdynski.grzegorz@gmail.com')
username_entry.grid(column=1, row=2, columnspan=2)

password_entry = ttk.Entry(width=25)
password_entry.grid(column=1, row=3)

# Buttons
search_button = ttk.Button(text="Search", width=23, command=find_password)
search_button.grid(column=2, row=1)

password_button = ttk.Button(text="Generate Password", width=23, command=generate_password)
password_button.grid(column=2, row=3)

add_button = ttk.Button(text="Add", width=50, command=save_data)
add_button.grid(column=1, row=4, columnspan=2)

reset_button = ttk.Button(text="Reset", width=15, command=reset_data)
reset_button.grid(column=2, row=5, sticky="SE")

window.mainloop()
