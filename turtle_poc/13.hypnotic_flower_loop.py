from turtle import *

speed(0)
bgcolor("black")
colors = ['cyan', 'magenta', 'yellow']
hideturtle()

for i in range(120):
    goto(0,0)
    color(colors[i % 3])
    forward(100)
    left(45)
    circle(50)
    right(90)
    forward(100)

done()
