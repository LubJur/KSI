from tkinter import Tk, Canvas, Event, ttk


class WidthSketch:
    def __init__(self, window: Tk) -> None:
        self.canvas = Canvas(window, width=640, height=480)
        self.canvas.bind('<Button-1>', self.activate)
        self.canvas.pack()

        self.width_slider = ttk.Scale(window, from_=1, to=100)
        self.width_slider.pack()

    def activate(self, event: Event) -> None:
        self.canvas.bind('<B1-Motion>', self.paint)
        self.last_x, self.last_y = event.x, event.y

    def paint(self, event: Event) -> None:
        x, y = event.x, event.y

        width = self.width_slider.get()
        self.canvas.create_line(self.last_x, self.last_y, x, y, width=width)
        self.last_x, self.last_y = x, y

        # In case of greater width, place an oval to cover unwanted artifacts.
        # Try to remove the next three lines and see what happens.
        if width > 3:
            r = (width-1) / 2
            self.canvas.create_oval(x-r, y-r, x+r, y+r, fill='black')


window = Tk()
window.title("WidthSketch")
sketch = WidthSketch(window)
window.mainloop()