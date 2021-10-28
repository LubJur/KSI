# https://tkdocs.com/tutorial/tree.html
# https://tkdocs.com/shipman/ttk-Treeview.html
# https://docs.python.org/3/library/tkinter.ttk.html#treeview
import json
import re
from tkinter import Tk, ttk, Toplevel, StringVar, BooleanVar
from typing import List

window = Tk()
# window.geometry("800x800")
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

    # https://stackoverflow.com/questions/48513729/remove-an-object-from-a-list-of-objects


def contact_window(contact_index):
    def save_data():
        print(contact.name, contact.email, contact.displayed)
        if name_var.get() != "":
            contact.name = name_var.get()
            contact.surname = surname_var.get()
            contact.displayed = displayed_var.get()
            contact.birthday = birthday_var.get()
            contact.set_email(email_var.get())
            contact.set_phone(phone_var.get())
            contact.note = note_var.get()
            print(contact.name, contact.surname, contact.displayed, contact.birthday, contact.email, contact.phone)
            add_to_tree()
            write_json()
        else:
            print("contact name is required")

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


def add_to_tree():
    last = len(contacts) - 1  # len starts at 1
    if contacts[last].name != "":
        print(tree.insert(parent="", index="end", values=(contacts[last].name, contacts[last].phone, last)))


def delete_from_tree():
    selected = tree.selection()
    print(selected)
    removed_indexes = []
    for i in selected:
        print(i)
        print(tree.item(i)["values"])
        removed_indexes.append(int(i))
        tree.delete(i)
    removed_indexes.reverse()  # we need to delete from contacts backwards because we would get index out of range
    # TODO: see if adding atribute IDintree to Contact would be better
    # TODO: remove also from json
    for i in removed_indexes:
        contacts.pop(int(i))
    build_tree()
    write_json()
    print(contacts)


def sort_contacts(descending):
    # https://stackoverflow.com/questions/403421/how-to-sort-a-list-of-objects-based-on-an-attribute-of-the-objects
    contacts.sort(key=lambda i: i.name, reverse=descending)
    build_tree()


def add_contact():
    contacts.append(Contact("", "", "", "", "", "", ""))
    index_new = len(contacts) - 1
    contact_window(index_new)  # get last index of contacts
    print(contacts)
    # tree.insert(parent="", index="end", values=(contacts[index_new].displayed, contacts[index_new].phone, index_new))
    # tree.grid()


def open_selected():
    selected = tree.selection()
    print(selected)
    # https://stackoverflow.com/questions/30614279/python-tkinter-tree-get-selected-item-values
    for i in selected:
        print(tree.item(i))
        contact_window(int(i))
        # contact_window(tree.item(i)["values"][2])


def add_column(colnames):
    # colnames.append("note")
    if surname.get() and "surname" not in colnames:
        colnames.append("surname")
    if surname.get() == False and "surname" in colnames:
        colnames.remove("surname")

    if displayed.get() and "displayed" not in colnames:
        colnames.append("displayed")
    if displayed.get() == False and "displayed" in colnames:
        colnames.remove("displayed")

    if birthday.get() and "birthday" not in colnames:
        colnames.append("birthday")
    if birthday.get() == False and "birthday" in colnames:
        colnames.remove("birthday")

    if email.get() and "email" not in colnames:
        colnames.append("email")
    if email.get() == False and "email" in colnames:
        colnames.remove("email")

    if phone.get() and "phone" not in colnames:
        colnames.append("phone")
    if phone.get() == False and "phone" in colnames:
        colnames.remove("phone")

    if note.get() == False and "note" not in colnames:
        colnames.append("note")
    if note.get() == False and "note" in colnames:
        colnames.remove("note")
    print(colnames)

    # https://stackoverflow.com/questions/43142332/how-can-i-add-a-column-to-a-tkinter-treeview-widget
    # https://www.google.com/search?q=tkinter+treeview+add+column&oq=tkinter+tree+add+colum&aqs=chrome.1.69i57j0i22i30.5943j0j7&sourceid=chrome&ie=UTF-8
    print("pridavam column")
    tree.destroy()
    build_tree()


colnames = ["name"]


def build_tree():
    global tree
    print("staviam strom")
    tree = ttk.Treeview(window, columns=colnames)
    for i in colnames:
        tree.heading(column=i, text=i)
        tree.column(column=i)
    # https://www.py4u.net/discuss/20230
    tree.grid(row=0, rowspan=7)
    for i in range(len(contacts)):
        if contacts[i].name != "":
            tree.insert(parent="", index="end", iid=i)
        for j in colnames:
            # https://stackoverflow.com/questions/3253966/python-string-to-attribute
            tree.set(i, column=j, value=getattr(contacts[i], j))


def write_json():
    with open("contacts.json", "w") as file:
        # old_data = json.load(file)
        to_dump = {"contacts": []}
        for i in contacts:
            to_dump["contacts"].append({"name": i.name, "surname": i.surname, "displayed": i.displayed,
                                        "birthday": i.birthday, "email": i.email, "phone": i.phone, "note": i.note})
        json.dump(to_dump, file, indent=2)


contacts: List[Contact] = []
descending: bool = False

# we need to use BooleanVar instead of bool because clicking one button changes all values
surname = BooleanVar()
displayed = BooleanVar()
birthday = BooleanVar()
email = BooleanVar()
phone = BooleanVar()
note = BooleanVar()

with open("contacts.json", "r") as file:
    obj = json.load(file)
    print(obj)
    for i in obj["contacts"]:
        contacts.append(Contact(i["name"], i["surname"], i["displayed"], i["birthday"], i["email"], i["phone"],
                                i["note"]))
    print(contacts)
    build_tree()

open_selected = ttk.Button(window, text="open selected", command=open_selected)
open_selected.grid(row=0, column=2)

add_contact = ttk.Button(window, text="Add contact", command=add_contact)
add_contact.grid(row=1, column=2)

delete_contact = ttk.Button(window, text="Delete contact", command=delete_from_tree)
delete_contact.grid(row=2, column=2)

# https://stackoverflow.com/questions/6920302/how-to-pass-arguments-to-a-button-command-in-tkinter
descending_button = ttk.Button(window, text="Descending order", command=lambda: sort_contacts(True))
descending_button.grid(row=0, column=3)

ascending_button = ttk.Button(window, text="Ascending order", command=lambda: sort_contacts(False))
ascending_button.grid(row=1, column=3)

column_button = ttk.Button(window, text="Add columns", command=lambda: add_column(colnames))
column_button.grid(row=6, column=1)

surname_select = ttk.Checkbutton(window, text="Surnames", variable=surname)
surname_select.grid(row=0, column=1)

displayed_select = ttk.Checkbutton(window, text="Displayed", variable=displayed)
displayed_select.grid(row=1, column=1)

birthday_select = ttk.Checkbutton(window, text="Birthday", variable=birthday)
birthday_select.grid(row=2, column=1)

email_select = ttk.Checkbutton(window, text="Email", variable=email)
email_select.grid(row=3, column=1)

phone_select = ttk.Checkbutton(window, text="Phone", variable=phone)
phone_select.grid(row=4, column=1)

note_select = ttk.Checkbutton(window, text="Note", variable=note)
note_select.grid(row=5, column=1)

window.mainloop()
