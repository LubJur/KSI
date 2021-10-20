# https://tkdocs.com/tutorial/tree.html
# https://tkdocs.com/shipman/ttk-Treeview.html
# https://docs.python.org/3/library/tkinter.ttk.html#treeview
import json
from json import JSONEncoder
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

    def set_phone(self, phone):
        # https://regex101.com/
        if re.fullmatch(r"\+[0-9, ]+|[0-9, ]+", phone):
            print("telefon plati")
            self.phone = phone
        else:
            print("telefon neplati")

contacts: List[Contact] = []

tree = ttk.Treeview(window, columns=(0, 1))

tree.heading(0, text="Name")
tree.heading(1, text="Phone")


def contact_window(contact_index):

    def save_data():
        print(contact.name, contact.email, contact.displayed)
        contact.name = name_var.get()
        contact.surname = surname_var.get()
        contact.displayed = displayed_var.get()
        contact.birthday = birthday_var.get()
        contact.set_email(email_var.get())
        contact.set_phone(phone_var.get())
        contact.note = note_var.get()
        print(contact.name, contact.surname, contact.displayed, contact.birthday, contact.email, contact.phone)
        write_json()

    contact_window = Toplevel(window)
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
    birthday_var.set(contact.birthday)
    email_var.set(contact.email)
    phone_var.set(contact.phone)
    note_var.set(contact.note)

    text_name = ttk.Label(contact_window, text="Name:")
    name = ttk.Entry(contact_window, textvariable=name_var)
    text_name.grid(row=0, column=0)
    name.grid(row=0, column=1)

    text_surname = ttk.Label(contact_window, text="Surname:")
    surname = ttk.Entry(contact_window, textvariable=surname_var)
    text_surname.grid(row=1, column=0)
    surname.grid(row=1, column=1)

    text_displayed = ttk.Label(contact_window, text="Displayed:")
    displayed = ttk.Entry(contact_window, textvariable=displayed_var)
    text_displayed.grid(row=2, column=0)
    displayed.grid(row=2, column=1)

    text_birthday = ttk.Label(contact_window, text="Birthday:")
    birthday = ttk.Entry(contact_window, textvariable=birthday_var)
    text_birthday.grid(row=3, column=0)
    birthday.grid(row=3, column=1)

    text_email = ttk.Label(contact_window, text="E-mail:")
    email = ttk.Entry(contact_window, textvariable=email_var)
    text_email.grid(row=4, column=0)
    email.grid(row=4, column=1)

    text_phone = ttk.Label(contact_window, text="Phone:")
    phone = ttk.Entry(contact_window, textvariable=phone_var)
    text_phone.grid(row=5, column=0)
    phone.grid(row=5, column=1)

    text_note = ttk.Label(contact_window, text="Note:")
    note = ttk.Entry(contact_window, textvariable=note_var)
    text_note.grid(row=6, column=0)
    note.grid(row=6, column=1)

    save_button = ttk.Button(contact_window, text="Save", command=save_data)
    save_button.grid(row=7, column=0)


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


def write_json():
    with open("contacts.json", "w") as file:
        #old_data = json.load(file)
        to_dump = {"contacts": []}
        for i in contacts:
            to_dump["contacts"].append({"name": i.name, "surname": i.surname, "displayed": i.displayed,
                                        "birthday": i.birthday, "email": i.email, "phone": i.phone, "note": i.note})
        print(to_dump)
        json.dump(to_dump, file, indent=2)


with open("contacts.json", "r") as file:
    obj = json.load(file)
    print(obj)
    for i in obj["contacts"]:
        contacts.append(Contact(i["name"], i["surname"], i["displayed"], i["birthday"], i["email"], i["phone"],
                                i["note"]))
    print(type(contacts[0]))
    update_tree()


button = ttk.Button(window, text="open selected", command=open_selected)
button.grid(row = 1)

window.mainloop()