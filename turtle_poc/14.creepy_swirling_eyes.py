from turtle import *
import math

speed(0)
bgcolor("black")
colors = ['white', 'gray']
hideturtle()

for i in range(150):
    goto(0,0)
    color(colors[i % 2])
    forward(120)
    left(i % 360)
    circle(30 + (i % 10))
    right(180)
    forward(120)

done()
