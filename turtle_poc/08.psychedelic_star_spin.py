import turtle, colorsys

t = turtle.Turtle()
t.speed(0)
t.width(2)
turtle.bgcolor("black")

h = 0

for i in range(300):
    t.pencolor(colorsys.hsv_to_rgb(h, 1, 1))
    t.forward(200)
    t.left(170)
    h += 0.01

turtle.done()
