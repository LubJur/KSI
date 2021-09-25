from turtle import Turtle
julie = Turtle()

for i in range(3,10):
    for j in range(i):
        julie.fd(100)
        julie.lt(360/i)