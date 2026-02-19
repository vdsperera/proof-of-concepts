import turtle, colorsys

t = turtle.Turtle()
t.speed(0)
t.width(2)
turtle.bgcolor("black")

h = 0
size = 1

for i in range(300):
    t.pencolor(colorsys.hsv_to_rgb(h, 1, 1))
    t.forward(size)
    t.left(59)
    h += 0.01
    size += 0.5  # makes it feel like it’s pulling you in

turtle.done()
