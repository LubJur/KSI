from tkinter import Tk, ttk, StringVar

window = Tk()

number = StringVar(value="10")
label = ttk.Label(window, textvariable=number)
label.pack()

def increase():
    number.set(int(number.get()) + 1)

def decrease():
    number.set(int(number.get()) - 1)

increase_button = ttk.Button(window, text="+ 1", command = increase)
increase_button.pack()

decrease_button = ttk.Button(window, text="- 1", command = decrease)
decrease_button.pack()

window.mainloop()