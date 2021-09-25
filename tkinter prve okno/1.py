from tkinter import Tk, ttk

window = Tk()

label1 = ttk.Label(window, text="Prvy label", foreground="white", background="blue")
label2 = ttk.Label(window, text="Druhy label", foreground="white", background="blue")
label3 = ttk.Label(window, text="Treti label", foreground="white", background="blue")
label4 = ttk.Label(window, text="Stvrty label, dlhsi text", foreground="white", background="blue")
label5 = ttk.Label(window, text="Piaty label", foreground="white", background="blue")

label1.grid(column=1, row=1)
label2.grid(column=1, row=2)
label3.grid(column=1, row=3)
label4.grid(column=1, row=4)
label5.grid(column=2, row=1, sticky="wens", rowspan=4)

window.mainloop()