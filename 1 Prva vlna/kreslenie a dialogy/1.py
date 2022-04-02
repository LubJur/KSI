from tkinter import Tk, Canvas, Event, colorchooser, ttk


class ColorSketch:
    def __init__(self, window: Tk) -> None:
        self.canvas = Canvas(window, width=640, height=480)
        self.canvas.bind('<Button-1>', self.activate)
        self.canvas.pack()

        self.color = 'black'
        ttk.Button(
            window,
            text='Choose Color',
            command = self.choose_color
        ).pack()

    def choose_color(self) -> None:
        self.color = colorchooser.askcolor()[1]

    def activate(self, event: Event) -> None:
        self.canvas.bind('<B1-Motion>', self.paint)
        self.last_x, self.last_y = event.x, event.y

    def paint(self, event: Event) -> None:
        x, y = event.x, event.y
        self.canvas.create_line(
            self.last_x, self.last_y,
            x, y,
            fill=self.color
        )
        self.last_x, self.last_y = x, y


window = Tk()
window.title = "ColorSketch"
sketch = ColorSketch(window)
window.mainloop()