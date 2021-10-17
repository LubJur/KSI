# https://tkdocs.com/tutorial/tree.html
# https://tkdocs.com/shipman/ttk-Treeview.html
# https://docs.python.org/3/library/tkinter.ttk.html#treeview
import json
import re
from tkinter import Tk, ttk, Toplevel, StringVar
from typing import List

window = Tk()
#window.geometry("800x800")
window.resizable(False, False)


class Contact:
    def __init__(self, name, surname, displayed, birthday, email, phone, note):
        self.name = name
        self.surname = surname
        self.displayed = displayed
        self.birthday = birthday
        self.email = email
        self.phone = phone
        self.note = note

    def set_email(self, email):
        # https://emailregex.com/
        # https://www.geeksforgeeks.org/check-if-email-address-valid-or-not-in-python/
        if re.fullmatch(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email):
            print("plati")
            self.email = email
        else:
            print("E-mail is invalid")


contacts: List[Contact] = []

tree = ttk.Treeview(window, columns=(0, 1))

tree.heading(0, text="Name")
tree.heading(1, text="Phone")

def contact_window(contact_index):
    """
    I store the index of object Contact in list contacts
    inside of the tree because tree stores it as a str
    """
    new_window = Toplevel(window)
    contact = contacts[contact_index]

    name = ttk.Label(new_window, text=f"Name: {contact.name}")
    phone = ttk.Label(new_window, text=contact.phone)
    phone_var = StringVar()
    input_phone = ttk.Entry(new_window, textvariable=phone_var)
    #edit_button = ttk.Button(new_window, text="edit", command=lambda: contact.set_email(str(phone_var.get())))
    edit_button = ttk.Button(new_window, text="edit", command=lambda: edit_window(contact_index))
    # https://stackoverflow.com/questions/6920302/how-to-pass-arguments-to-a-button-command-in-tkinter
    name.grid(row=1)
    phone.grid(row=2)
    input_phone.grid(row=3)
    edit_button.grid(row=4)

    # TODO: vracanie udajov z tohto okna
    # TODO: funkcia na zapisovanie udajov do json suboru, vykona sa po zatvoreni okna kontaktu

def edit_window(contact_index):
    edit_window = Toplevel(window)
    contact = contacts[contact_index]

    name_var = StringVar()
    surname_var = StringVar()
    displayed_var = StringVar()
    birthday_var = StringVar()
    email_var = StringVar()
    phone_var = StringVar()
    note_var = StringVar()

    name_var.set(contact.name)
    surname_var.set(contact.surname)
    displayed_var.set(contact.displayed)
    email_var.set(contact.email)
    phone_var.set(contact.phone)
    note_var.set(contact.note)

    text_name = ttk.Label(edit_window, text="Name:")
    name = ttk.Entry(edit_window, textvariable=name_var)
    text_name.grid(row=0, column=0)
    name.grid(row=0, column=1)

    text_surname = ttk.Label(edit_window, text="Surname:")
    surname = ttk.Entry(edit_window, textvariable=surname_var)
    text_surname.grid(row=1, column=0)
    surname.grid(row=1, column=1)

    text_displayed = ttk.Label(edit_window, text="Displayed:")
    displayed = ttk.Entry(edit_window, textvariable=displayed_var)
    text_displayed.grid(row=2, column=0)
    displayed.grid(row=2, column=1)

    text_birthday = ttk.Label(edit_window, text="Birthday:")
    birthday = ttk.Entry(edit_window, textvariable=birthday_var)
    text_birthday.grid(row=3, column=0)
    birthday.grid(row=3, column=1)

    text_email = ttk.Label(edit_window, text="E-mail:")
    email = ttk.Entry(edit_window, textvariable=email_var)
    text_email.grid(row=4, column=0)
    email.grid(row=4, column=1)

    text_phone = ttk.Label(edit_window, text="Phone:")
    phone = ttk.Entry(edit_window, textvariable=phone_var)
    text_phone.grid(row=5, column=0)
    phone.grid(row=5, column=1)

    text_note = ttk.Label(edit_window, text="Note:")
    note = ttk.Entry(edit_window, textvariable=note_var)
    text_note.grid(row=6, column=0)
    note.grid(row=6, column=1)

    save_button = ttk.Button(edit_window, text="Save", command=lambda: save_data(name_var.get(), surname_var.get(), displayed_var.get(), birthday_var.get(), email_var.get(), phone_var.get(), note_var.get(), contact_index))
    save_button.grid(row=7, column=0)

def save_data(name_var, surname_var, displayed_var, birthday_var, email_var, phone_var, note_var, contact_index):
    print(name_var, surname_var, displayed_var, birthday_var, email_var, phone_var, note_var, contact_index)
    # TODO: toto je dost sprosty sposob ukladania dat, pozri na internete tkinter form

def update_tree():
    for i in range(len(contacts)):
        tree.insert(parent="", index="end", values=(contacts[i].displayed, contacts[i].phone, i))
    tree.grid()

def open_selected():
    selected = tree.selection()
    print(selected)
    # https://stackoverflow.com/questions/30614279/python-tkinter-tree-get-selected-item-values
    for i in selected:
        print(tree.item(i))
        contact_window(tree.item(i)["values"][2])

with open("contacts.json", "r") as file:
    obj = json.load(file)
    for i in obj["contacts"]:
        contacts.append(Contact(i["name"], i["surname"], i["displayed"], i["birthday"], i["email"], i["phone"],
                                i["note"]))
    print(type(contacts[0]))
    update_tree()

button = ttk.Button(window, text="open selected", command=open_selected)
button.grid(row = 1)

window.mainloop()