# https://towardsdatascience.com/easy-steps-to-plot-geographic-data-on-a-map-python-11217859a2db
# https://greenvillagedotblog.wordpress.com/2018/08/05/decoding-nmea-sentences/
from tkinter import Tk, Canvas, PhotoImage, ttk, StringVar

window = Tk()
canvas = Canvas(window, width=800, height=800)
canvas.grid(row=0, column=0, columnspan=5)
window.resizable(False, False)
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
    """
    print(TOP > decimal > BOTTOM)
    print(RIGHT > decimal > LEFT)
    # TODO: dokonci overovanie nmea ci moze byt
    if (BOTTOM <= decimal or decimal >= TOP) or (LEFT <= decimal or decimal >= RIGHT):
        print("aset pass")
    else:
        print("aset fail")
    assert (BOTTOM < degrees + minutes / 60 < TOP or LEFT < degrees + minutes / 60 < RIGHT), "NMEA data is larger than " \
                                                                                             "map size "
    """
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

def time_translate(time):
    hours = time[:2]
    minutes = time[2:4]
    seconds = time[4:]
    return str(hours + ":" + minutes + ":" + seconds)

def decimal_to_lat_long(decimal):
    decimal = str(decimal)
    degrees = int(decimal[:2])
    minutes = int((float(decimal) - degrees) * 60)
    seconds = int((float(decimal) - degrees - minutes/60) * 3600)
    return str(f"{degrees}°{minutes}'{seconds}\"")

drawn_points = []

class Point:
    def __init__(self, canvas, x, y, time, lat, long):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.time = time
        self.lat = lat
        self.long = long
        self.point = canvas.create_oval(0, 0, 0, 0, width=0)

    def delete_point(self):
        print("vymazavam objekt:", self)
        canvas.delete(self.point)
        if self in drawn_points:
            drawn_points.remove(self)

    def draw_point(self):
        self.point = canvas.create_oval(self.x, self.y, self.x + 5, self.y + 5, fill="red", width=0)
        drawn_points.append(self)



with open("log.txt", "r") as file:
    list_of_xy = []
    line = file.readline()
    while line != "":
        line = file.readline()
        if line.startswith("$GPRMC"):
            line = line.split(",")
            x = float(line[5])
            y = float(line[3])
            time = time_translate(line[1])
            x = nmea_to_decimal(x)
            y = nmea_to_decimal(y)
            lat = decimal_to_lat_long(y)
            long = decimal_to_lat_long(x)
            x = coordinates_to_xy(x)
            y = coordinates_to_xy(y)
            list_of_xy.append([x, y, time, lat, long])
    assert list_of_xy != [], "Data file is invalid"


now_point = StringVar(value="0")
time = StringVar(value="0")
latitude = StringVar(value="0")
longitude = StringVar(value="0")


def next_point():
    if int(now_point.get()) < len(list_of_xy)-1:
        points[int(now_point.get())].draw_point()
        time.set(points[int(now_point.get())].time)
        latitude.set(points[int(now_point.get())].lat)
        longitude.set(points[int(now_point.get())].long)
        now_point.set(int(now_point.get()) + 1)
        value_slider.set(now_point.get())
        canvas.update_idletasks()


def back_point():
    if int(now_point.get()) > 0:
        popped_exists = drawn_points.pop()
        popped_exists.delete_point()
        #points[int(now_point.get())].delete_point()
        now_point.set(int(now_point.get()) - 1)
        canvas.update_idletasks()
        time.set(points[int(now_point.get())].time)
        latitude.set(points[int(now_point.get())].lat)
        longitude.set(points[int(now_point.get())].long)
        value_slider.set(now_point.get())


def draw_all():
    for i in points:
        i.draw_point()
    time.set(points[int(now_point.get())].time)
    latitude.set(points[int(now_point.get())].lat)
    longitude.set(points[int(now_point.get())].long)
    now_point.set(len(list_of_xy) - 1)  # -1 because len(list_of_xy) returns 4969 but the last index has value 4968
    value_slider.set(now_point.get())


def delete_all():
    canvas.delete("all")
    canvas.create_image(0, 0, image=bg, anchor="nw")
    value_slider.set(0)
    now_point.set(0)
    time.set(points[int(now_point.get())].time)
    latitude.set(points[int(now_point.get())].lat)
    longitude.set(points[int(now_point.get())].long)


def slider_change(event):
    #print(int(now_point.get()))
    #print(int(value_slider.get()))
    time.set(points[int(now_point.get())].time)
    latitude.set(points[int(now_point.get())].lat)
    longitude.set(points[int(now_point.get())].long)
    if int(now_point.get()) < int(value_slider.get()):
        now_point.set(int(value_slider.get()))
        points[int(now_point.get())].draw_point()
        #next_point()
    else:
        """
        I haven't found a better way to go backwards without leaving artefacts than
        deleting everything and redrawing until new point number
        """
        now_point.set(int(value_slider.get()))
        points[int(now_point.get())].delete_point()
        canvas.delete("all")
        canvas.create_image(0, 0, image=bg, anchor="nw")
        for i in points[:int(now_point.get())]:
            i.draw_point()
    #canvas.update_idletasks()
        #back_point()
    """
    now_point.set(int(value_slider.get()))
    points[int(now_point.get())].draw_point()
    canvas.update_idletasks()
    """

points = []

for i in range(len(list_of_xy)):
    points.append(Point(canvas, list_of_xy[i][0], list_of_xy[i][1], list_of_xy[i][2], list_of_xy[i][3], list_of_xy[i][4]))

next_button = ttk.Button(window, text="+1", command=next_point)
next_button.grid(row=1, column=3, sticky="w")

back_button = ttk.Button(window, text="-1", command=back_point)
back_button.grid(row=1, column=1, sticky="e")

draw_all = ttk.Button(window, text="Draw all", command=draw_all)
draw_all.grid(row=1, column=4)

delete_all = ttk.Button(window, text="Delete all", command=delete_all)
delete_all.grid(row=1, column=0)

value_slider = ttk.Scale(window, from_=0, to=len(list_of_xy)-1, command=slider_change)  # -1 because len(list_of_xy) returns 4969 but the last index has value 4968
value_slider.grid(row=2, column=0, columnspan=5, sticky="nsew")

text_point_label = ttk.Label(window, text="Point No.")
text_point_label.grid(row=3, column=1)

point_label = ttk.Label(window, textvariable=now_point)
point_label.grid(row=3, column=2)

text_time_label = ttk.Label(window, text="Time (UTC)")
text_time_label.grid(row=4, column=1)

time_label = ttk.Label(window, textvariable=time)
time_label.grid(row=4, column=2)

text_latidude_label = ttk.Label(window, text="Latitude")
text_latidude_label.grid(row=5, column=1)

latidude_label = ttk.Label(window, textvariable=latitude)
latidude_label.grid(row=5, column=2)

text_longitude_label = ttk.Label(window, text="Longitude")
text_longitude_label.grid(row=6, column=1)

longitude_label = ttk.Label(window, textvariable=longitude)
longitude_label.grid(row=6, column=2)

window.mainloop()
