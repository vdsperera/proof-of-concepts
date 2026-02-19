import turtle, colorsys

t = turtle.Turtle()
t.speed(0)
t.width(2)
turtle.bgcolor("black")

h = 0

for i in range(360):
    t.pencolor(colorsys.hsv_to_rgb(h, 1, 1))
    t.forward(i * 0.6)
    t.left(121)  # odd number angles confuse perception
    h += 0.012

turtle.done()
