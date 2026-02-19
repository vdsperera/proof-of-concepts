import turtle, colorsys

t = turtle.Turtle()
t.speed(0)
t.width(2)
turtle.bgcolor("black")

h = 0

for i in range(400):
    t.pencolor(colorsys.hsv_to_rgb(h, 1, 1))
    t.forward(i * 0.4)
    t.right(61)
    h += 0.008

turtle.done()
