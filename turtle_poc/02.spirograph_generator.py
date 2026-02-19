import turtle

t = turtle.Turtle()
t.speed(0)
turtle.bgcolor("black")
t.color("red")

for i in range(36):
    t.circle(100)
    t.right(10)

turtle.done()
