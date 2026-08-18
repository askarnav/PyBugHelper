from tkinter import *
from tkinter import messagebox
import pyperclip
from random import randint, choice, shuffle
import json



# Only used for reading not writing to a file
def open_and_read(filepath):
    with open(filepath) as file:
        file_data = file.read()
    return file_data




def manager():
    # --------------------------- REMOVE ------------------------------- #
    def remove():
        site_name = website.get()
        if len(site_name) == 0:
            messagebox.showinfo(title="Password manager", message="Please type a site in website entry.")
        else:
            try:
                with open("passwords.json", "r") as passwords:
                    data = json.load(passwords)

                if site_name in data:
                    data.pop(site_name)

                    with open("passwords.json", "w") as passwords:
                        json.dump(data, passwords, indent=4)

                    messagebox.showinfo(title="Removed", message=f"{site_name} deleted successfully!")
                else:
                    messagebox.showinfo(title="Not Found", message=f"{site_name} not in saved data.")

            except FileNotFoundError:
                messagebox.showinfo(title="Password manager", message="No data yet")

    # ---------------------------- INFORMATION METHOD ----------------------------#
    def show_info():
        try:
            with open("passwords.json") as passwords:
                messagebox.showinfo(title="MyPass", message=passwords.read())
        except FileNotFoundError:
            messagebox.showinfo(title="Password manager", message="No data yet")

    # ---------------------------- SEARCH METHOD ---------------------------- #
    def search():
        website_name = website.get()
        with open("passwords.json") as code_file:
            data = json.load(code_file)
        if len(website_name) <= 0:
            messagebox.showinfo(title="RuntimeError", message="Enter the website name first!")
        elif website_name not in data:
            messagebox.showinfo(title="SiteNotFound!", message="You have not added this info yet!")
        else:
            for site in data:
                if site == website_name:
                    messagebox.showinfo(title=f"{website_name}",
                                        message=f"Password: {data[website_name]["password"]} \n Email/Username: {data[website_name]["email"]}")
                    break

    # ---------------------------- PASSWORD GENERATOR ------------------------------- #

    def generate_password():
        letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                   'u',
                   'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O',
                   'P',
                   'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

        password_letters = [choice(letters) for _ in range(randint(8, 10))]
        password_numbers = [choice(numbers) for _ in range(randint(2, 4))]
        password_symbols = [choice(symbols) for _ in range(randint(2, 4))]

        password_list = password_symbols + password_numbers + password_letters

        shuffle(password_list)
        password_text = "".join(password_list)

        password.delete(0, END)
        password.insert(0, password_text)
        pyperclip.copy(password.get())

    # ---------------------------- SAVE PASSWORD ------------------------------- #
    def save():
        website_name = website.get()
        email_name = email.get()
        code = password.get()

        new_data = {
            website_name: {
                "email": email_name,
                "password": code,
            }
        }

        if len(website_name) == 0 or len(code) == 0:
            messagebox.showinfo(title="Oops", message="Please make sure you haven't left any fields empty.")
        else:
            to_save = messagebox.askokcancel(title=f"Confirmation for {website_name}",
                                             message="Please confirm the details! \n  "
                                                     f"Email: {email_name} \n Password: {code}")
            if to_save:
                try:
                    with open("passwords.json", "r") as file:
                        data = json.load(file)
                except FileNotFoundError:
                    with open("passwords.json", "w") as file:
                        json.dump(new_data, file, indent=4)
                else:
                    data.update(new_data)

                    with open("passwords.json", "w") as file:
                        json.dump(data, file, indent=4)
                finally:
                    website.delete(0, END)
                    password.delete(0, END)
                    messagebox.showinfo(title="Done!", message="Site added successfully!")

    # ---------------------------- UI SETUP ------------------------------- #


    white = "#FFFFFF"

    # Window
    window = Tk()
    window.title("Password manager")
    window.config(padx=50, pady=20, bg=white)

    # Canvas
    canvas = Canvas(width=200, height=200, bg=white, highlightthickness=0)
    logo_img = PhotoImage(file="C:/Users/Arnav/Desktop/Coding/Files/Intermediate (Sections 15 to 32)/UI apps with tkinter/Password manager/logo.png")
    canvas.create_image(100, 100, image=logo_img)
    canvas.grid(column=1, row=0)

    # Labels Layout
    website_label = Label(text="Website: ", bg=white)
    email_label = Label(text="Email/Username: ", bg=white)
    password_label = Label(text="Password: ", bg=white)
    website_label.grid(row=1, column=0)
    email_label.grid(row=2, column=0)
    password_label.grid(row=3, column=0)

    # Entries
    website = Entry(width=35)
    website.focus()
    email = Entry(width=35)
    email.insert(0, "@gmail.com")
    password = Entry(width=21)
    website.grid(row=1, column=1, columnspan=2)
    email.grid(row=2, column=1, columnspan=2)
    password.grid(row=3, column=1)

    # Buttons
    generate_button = Button(text="Generate Password", command=generate_password)
    generate_button.grid(row=3, column=2)
    add_button = Button(text="Add", width=35, command=save)
    add_button.grid(row=4, column=1, columnspan=2)
    search_button = Button(text="Search", command=search)
    search_button.grid(row=1, column=3)
    data_button = Button(text="Show your data", command=show_info)
    data_button.grid(row=2, column=2, columnspan=2)
    remove_button = Button(text="Remove", command=remove)
    remove_button.grid(row=4, column=4)

    window.mainloop()




def log_in(email, password, pass_in, email_in):
    if email_in == email and pass_in == password:
        return True
    else:
        return False


def writer(file, string):
    with open(file, "w") as x:
        x.write(string)


def add(file, string):
    with open(file, "a") as x:
        x.write(string)
