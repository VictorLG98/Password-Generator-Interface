from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
letras = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
          'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

numbers = ['1', '2', '3', '4', '5', '6', '7', '8', '9']


def pass_gen():
    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    pass_letters = [random.choice(letras) for _ in range(nr_letters)]
    pass_symbols = [random.choice(letras) for _ in range(nr_symbols)]
    pass_numbers = [random.choice(letras) for _ in range(nr_numbers)]

    pass_list = pass_letters + pass_symbols + pass_numbers
    random.shuffle(pass_list)

    password = "".join(pass_list)
    pass_text.delete(0, END)
    pass_text.insert(0, password)
    pyperclip.copy(password)
# ---------------------------- SAVE PASSWORD ------------------------------- #


def save():
    new_data = {
        web_text.get().strip(): {
            "email": email_text.get().strip(),
            "password": pass_text.get().strip(),
        }
    }

    if web_text.get().isspace() or web_text.get() == "" or email_text.get().isspace() or email_text.get() == "" or pass_text.get().isspace() or pass_text.get() == "":
        messagebox.showerror(title="Error", message="Debes rellenar todos los campos")
    else:
        is_ok = messagebox.askokcancel(title=web_text.get(),
                                           message=f'Estos son los detalles: \nEmail: {email_text.get()}'
                                                   f'\nPassword: {pass_text.get()} \n¿Guardar?')
        if is_ok:
            try:
                with open('info.json', mode='r') as f:
                    data = json.load(f)
                    data.update(new_data)
            except FileNotFoundError:
                with open("info.json", mode="w") as f:
                    json.dump(new_data, f, indent=4)
            else:
                data.update(new_data)

                with open("info.json", mode='w') as f:
                    json.dump(data, f, indent=4)
            finally:
                web_text.delete(0, END)
                pass_text.delete(0, END)


def search():
    web = web_text.get()
    try:
        with open('info.json', mode='r') as f:
            data = json.load(f)
    except FileNotFoundError:
        messagebox.showerror(title="Error", message="No existe el fichero")
    else:
        if web in data:
            email = data[web]["email"]
            password = data[web]["password"]
            messagebox.showinfo("Búsqueda", message=f'Email: {email}\nPassword: {password}')
        else:
            messagebox.showerror(title="Error", message=f"No hay detalles sobre la web: {web}")

# ---------------------------- UI SETUP ------------------------------- #


window = Tk()
window.title("Password Manager")
window.config(padx=20, pady=20, bg='white')

canvas = Canvas(width=200, height=200, highlightthickness=0, bg='white')
logo_img = PhotoImage(file='logo.png')
canvas.create_image(100, 100, image=logo_img)
canvas.grid(column=1, row=1)

# Labels
web_label = Label(window, text="Website:", fg='black', highlightthickness=0, font=('Courier', 11, 'bold'), bg='white')
web_label.grid(column=0, row=2)
email_label = Label(window, text="Email/Username:", fg='black', highlightthickness=0, font=('Courier', 11, 'bold'), bg='white')
email_label.grid(column=0, row=3, pady=5)
pass_label = Label(window, text="Password:", fg='black', highlightthickness=0, font=('Courier', 11, 'bold'), bg='white')
pass_label.grid(column=0, row=4, pady=2)

# Texts
web_text = Entry(width=40)
web_text.focus()
web_text.grid(column=1, row=2)
email_text = Entry(width=40)
email_text.insert(0, "vitrexesp@gmail.com")
email_text.grid(column=1, row=3)
pass_text = Entry(width=40)
pass_text.grid(column=1, row=4)

# Buttons

pass_button = Button(text="Generate Password", font=('Courier', 9, 'bold'), highlightthickness=0, command=pass_gen)
pass_button.grid(column=3, row=4, padx=10)

add_button = Button(text='Add', font=('Courier', 9, 'bold'), highlightthickness=0, width=36, command=save)
add_button.grid(column=1, row=5, pady=10)

search_button = Button(text='Search', font=('Courier', 9, 'bold'), highlightthickness=0, width=15, command=search)
search_button.grid(column=3, row=2)

window.mainloop()
