# https://towardsdatascience.com/easy-steps-to-plot-geographic-data-on-a-map-python-11217859a2db
# https://greenvillagedotblog.wordpress.com/2018/08/05/decoding-nmea-sentences/
from tkinter import Tk, Canvas, PhotoImage, ttk, StringVar

window = Tk()
canvas = Canvas(window, width=800, height=800)
canvas.grid(row=0, column=0, columnspan=2)
bg = PhotoImage(file="map.gif")
canvas.create_image(0, 0, image=bg, anchor="nw")

# approximate coordinates of map edges
LEFT = 16.5948
RIGHT = 16.61148
TOP = 49.21864
BOTTOM = 49.20759
SIZE_X = RIGHT - LEFT
SIZE_Y = TOP - BOTTOM


def nmea_to_decimal(nmea) -> float:
    nmea = str(nmea)
    if nmea[0] == 0:  # tiez by mohlo byt nmea.startswith("0")
        degrees = float(nmea[0:3])
        minutes = float(nmea[3:])
    else:
        degrees = float(nmea[0:2])
        minutes = float(nmea[2:])
    return degrees + minutes / 60


def coordinates_to_xy(coordinate):
    """
    coordinates calculation needs to be different
    for x and y axis because the higher irl coodinate
    is on the top of the map and tkinter canvas starts
    at top-left so the y axis needs to be flipped horizontally
    """
    if coordinate < 30:  #
        proportion_x = coordinate - LEFT
        return proportion_x / SIZE_X * 800
    else:
        proportion_y = coordinate - BOTTOM
        return abs((proportion_y / SIZE_Y * 800) - 800)


class Point:
    def __init__(self, canvas, x, y):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.point = canvas.create_oval(self.x, self.y, self.x + 5, self.y + 5, fill="yellow")

    def delete_point(self):
        canvas.delete(self)

    def draw_point(self):
        canvas.create_oval(self.x, self.y, self.x + 5, self.y + 5, fill="yellow")


"""
def draw_on_canvas(self, x,y):
    canvas.create_oval(x, y, x+10, y+10, fill = "green")
    x += 10
    y += 10
    self.after(10, draw_on_canvas(self, x, y))
"""

with open("log.txt", "r") as file:
    list_of_xy = []
    line = file.readline()
    while line != "":
        line = file.readline()
        if line.startswith("$GPRMC"):
            line = line.split(",")
            x = float(line[5])
            y = float(line[3])
            x = coordinates_to_xy(nmea_to_decimal(x))
            y = coordinates_to_xy(nmea_to_decimal(y))
            list_of_xy.append([x, y])

now_point = StringVar(value="0")


def next_point():
    now_point.set(int(now_point.get()) + 1)
    x = list_of_xy[int(now_point.get())][0]
    y = list_of_xy[int(now_point.get())][1]
    canvas.create_oval(x, y, x + 10, y + 10, fill="red")
    canvas.update_idletasks()


def back_point():
    if int(now_point.get()) > 0:
        now_point.set(int(now_point.get()) - 1)


def slider_change(event):
    now_point.set(int(value_slider.get()))
    x = list_of_xy[int(now_point.get())][0]
    y = list_of_xy[int(now_point.get())][1]
    canvas.create_oval(x, y, x + 10, y + 10, fill="red")
    canvas.update_idletasks()

points = []
for i in range(int(now_point.get())):
    points.append(Point(canvas, list_of_xy[i][0], list_of_xy[i][1]))
    print(points)

"""

print(x, y)
canvas.create_oval(x, y, x + 10, y + 10, fill="red")
point1 = Point(canvas, x, y)
point1.draw_point()
"""
next_button = ttk.Button(window, text="+1", command=next_point)
next_button.grid(row=1, column=1)

back_button = ttk.Button(window, text="-1", command=back_point)
back_button.grid(row=1, column=0)

value_slider = ttk.Scale(window, from_=0, to=len(list_of_xy)-1, command=slider_change)
value_slider.grid(row=2, column=1)

label = ttk.Label(window, textvariable=now_point)
label.grid(row=2, column=0)

window.mainloop()
