import turtle

t = turtle.Turtle()
t.speed(0)

def square(size):
    if size < 10:
        return
    for _ in range(4):
        t.forward(size)
        t.right(90)
    t.right(10)
    square(size - 10)

square(200)
turtle.done()
