import turtle
import math
import time

t = turtle.Turtle()
t.speed(0)
turtle.bgcolor("black")
t.color("white")
t.width(2)

# Draw face
t.penup()
t.goto(0, -100)
t.pendown()
t.circle(100)

# Function to draw eyes with oscillation
def draw_eyes(offset):
    for x, y in [(-40, 50), (40, 50)]:
        t.penup()
        t.goto(x, y + math.sin(offset)*10)
        t.pendown()
        t.dot(30, "white")

# Draw mouth
t.penup()
t.goto(-60, -40)
t.pendown()
t.setheading(-60)
t.circle(80, 120)

# Animate eyes
for i in range(100):
    t.clear()
    t.penup()
    t.goto(0, -100)
    t.pendown()
    t.circle(100)  # face
    draw_eyes(i/5)
    t.penup()
    t.goto(-60, -40)
    t.pendown()
    t.setheading(-60)
    t.circle(80, 120)
    t.hideturtle()
    turtle.update()
    time.sleep(0.05)

turtle.done()
