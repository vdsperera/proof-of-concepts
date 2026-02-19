import turtle

t = turtle.Turtle()
t.speed(0)
turtle.bgcolor("black")
t.color("cyan")

for i in range(200):
    t.forward(i * 2)
    t.right(91)

turtle.done()
