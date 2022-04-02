from tkinter import Tk, ttk

window = Tk()


def create_pyramid(height: int) -> None:
    black_count = height - 1
    yellow_count = 1

    for i in range(height):

        for j in range(black_count):
            left_rectangle = ttk.Label(window, foreground="black", background="black", padding=(10, 5), relief="raised")
            left_rectangle.grid(row=i, column=j)

            right_rectangle = ttk.Label(window, foreground="black", background="black", padding=(10, 5), relief="raised")
            right_rectangle.grid(row=i, column = yellow_count + black_count + j)

        for j in range(yellow_count):
            middle_rectangle = ttk.Label(window, foreground="blue", background="yellow", padding=(10, 5), relief="raised")
            middle_rectangle.grid(row = i, column = black_count + j)

        black_count -= 1
        yellow_count += 2


create_pyramid(10)

window.mainloop()