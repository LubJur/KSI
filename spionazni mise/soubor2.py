# https://towardsdatascience.com/easy-steps-to-plot-geographic-data-on-a-map-python-11217859a2db
# https://greenvillagedotblog.wordpress.com/2018/08/05/decoding-nmea-sentences/
import tkinter
from tkinter import Tk, Canvas
#from turtle import ScrolledCanvas, RawTurtle, TurtleScreen, Turtle
import turtle


#turtle.up()
#turtle.bgpic("map.gif")
# pravy dolny roh:
# 49.20759, 16.61148
# lavy horny roh:
# 49.2186 =>  49°13'6.96" N
# 16.5948 =>  16°35'41.28" E
# 4912.588840  => 49°12'35.33'' N
# 01635.927160 => 16°35'55.63'' E
# rozdiel medzi rohu a surad N je 0.0927116 alebo 0°0'31.63''
# rozdiel medzi rohu a surad E je 0.2355284 alebo
# pozri sa na E: v desatinnom tvare je roh vacsi ale v stupnoch mensi ako surad E
#
# The format for NMEA coordinates is (d)ddmm.mmmm
# d=degrees and m=minutes
# There are 60 minutes in a degree so divide the minutes by 60 and add that to the degrees.
#
# For the Latitude=35.15 N
# 35.15/60 = .5858 N
#
# For the Longitude= 12849.52 E,
# 128+ 49.52/60 = 128.825333 E
# https://stackoverflow.com/questions/36254363/how-to-convert-latitude-and-longitude-of-nmea-format-data-to-decimal
def nmea_to_decimal(nmea) -> float:
    nmea = str(nmea)
    if nmea[0] == 0:  # tiez by mohlo byt nmea.startswith("0")
        degrees = float(nmea[0:3])
        minutes = float(nmea[3:])
    else:
        degrees = float(nmea[0:2])
        minutes = float(nmea[2:])
    return degrees + minutes/60

print(nmea_to_decimal(4912.588840))
print(nmea_to_decimal(01635.927160))

#turtle.done()
