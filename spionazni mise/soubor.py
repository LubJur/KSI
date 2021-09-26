# https://towardsdatascience.com/easy-steps-to-plot-geographic-data-on-a-map-python-11217859a2db
# https://greenvillagedotblog.wordpress.com/2018/08/05/decoding-nmea-sentences/
from tkinter import Tk, Canvas, PhotoImage, ttk, StringVar

window = Tk()
canvas = Canvas(window, width=800, height=800)
canvas.grid(row=0, column=0, columnspan=5)
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
    if nmea[0] == 0:
        degrees = float(nmea[0:3])
        minutes = float(nmea[3:])
    else:
        degrees = float(nmea[0:2])
        minutes = float(nmea[2:])
    decimal = degrees + minutes / 60
    print(TOP > decimal > BOTTOM)
    print(RIGHT > decimal > LEFT)
    # TODO: dokonci overovanie nmea ci moze byt
    if (BOTTOM <= decimal or decimal >= TOP) or (LEFT <= decimal or decimal >= RIGHT):
        print("aset pass")
    else:
        print("aset fail")
    assert (BOTTOM < degrees + minutes / 60 < TOP or LEFT < degrees + minutes / 60 < RIGHT), "NMEA data is larger than " \
                                                                                             "map size "
    return decimal


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
    def __init__(self, canvas, x, y, time):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.time = time
        #self.point = canvas.create_oval(self.x, self.y, self.x + 5, self.y + 5, fill="yellow")
        self.point = canvas.create_oval(0,0,0,0)

    def delete_point(self):
        print("som v delete_point")
        self.canvas.delete(self.point)

    def draw_point(self):
        self.point = canvas.create_oval(self.x, self.y, self.x + 5, self.y + 5, fill="red", width=0)
        self.point


"""
    def __str__(self):
        return str(self.oval)
"""

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
            time = line[1]
            x = coordinates_to_xy(nmea_to_decimal(x))
            y = coordinates_to_xy(nmea_to_decimal(y))
            list_of_xy.append([x, y, time])
    assert list_of_xy != [], "Data file is invalid"

# TODO: pridat do list_of_xy aj cas
# TODO: ukazovat stupne a cas v okne
now_point = StringVar(value="0")
time = StringVar(value="0")

def time_translate(time):
    hours = time[:2]
    minutes = time[2:4]
    seconds = time[4:]
    return str(hours + ":" + minutes + ":" + seconds)


def next_point():
    if int(now_point.get()) < len(list_of_xy):
        points[int(now_point.get())].draw_point()
        now_point.set(int(now_point.get()) + 1)
        time.set(time_translate(points[int(now_point.get())].time))
        value_slider.set(now_point.get())
        canvas.update_idletasks()


def back_point():
    if int(now_point.get()) > 0:
        points[int(now_point.get())].delete_point()
        now_point.set(int(now_point.get()) - 1)
        time.set(time_translate(points[int(now_point.get())].time))
        value_slider.set(now_point.get())
        canvas.update_idletasks()

def draw_all():
    for i in points:
        i.draw_point()
    value_slider.set(len(list_of_xy))
    now_point.set(len(list_of_xy))
    time.set(time_translate(points[int(now_point.get())].time))

def delete_all():
    canvas.delete("all")
    canvas.create_image(0, 0, image=bg, anchor="nw")
    value_slider.set(0)
    now_point.set(0)
    time.set(time_translate(points[int(now_point.get())].time))

def slider_change(event):
    print(int(now_point.get()))
    print(int(value_slider.get()))
    if int(now_point.get()) <= int(value_slider.get()):
        now_point.set(int(value_slider.get()))
        points[int(now_point.get())].draw_point()
        #next_point()
    else:
        now_point.set(int(value_slider.get()))
        points[int(now_point.get())].delete_point()
        canvas.delete("all")
        canvas.create_image(0, 0, image=bg, anchor="nw")
        for i in points[:int(now_point.get())]:
            i.draw_point()
    time.set(time_translate(points[int(now_point.get())].time))
    #canvas.update_idletasks()
        #back_point()
    """
    now_point.set(int(value_slider.get()))
    points[int(now_point.get())].draw_point()
    canvas.update_idletasks()
    """

points = []

for i in range(len(list_of_xy)):
    points.append(Point(canvas, list_of_xy[i][0], list_of_xy[i][1], list_of_xy[i][2]))
"""
for i in points:
    i.draw_point()


print(x, y)
canvas.create_oval(x, y, x + 10, y + 10, fill="red")
point1 = Point(canvas, x, y)
point1.draw_point()
"""

next_button = ttk.Button(window, text="+1", command=next_point)
next_button.grid(row=1, column=3, sticky="w")

back_button = ttk.Button(window, text="-1", command=back_point)
back_button.grid(row=1, column=1, sticky="e")

draw_all = ttk.Button(window, text="Draw all", command=draw_all)
draw_all.grid(row=1, column=4)

delete_all = ttk.Button(window, text="Delete all", command=delete_all)
delete_all.grid(row=1, column=0)

value_slider = ttk.Scale(window, from_=0, to=len(list_of_xy)-1, command=slider_change)
value_slider.grid(row=2, column=0, columnspan=5, sticky="nsew")

label = ttk.Label(window, textvariable=now_point)
label.grid(row=1, column=2)

time_label = ttk.Label(window, textvariable=time)
time_label.grid(row=3, column=0)

window.mainloop()
