import turtle, random

t = turtle.Turtle()
t.speed(0)
turtle.bgcolor("white")

colors = ["red", "blue", "green", "purple", "orange"]

for _ in range(500):
    t.color(random.choice(colors))
    t.forward(20)
    t.right(random.choice([0, 90, 180, 270]))

turtle.done()
