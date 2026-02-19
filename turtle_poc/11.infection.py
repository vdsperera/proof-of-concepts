import turtle
import random
import time

screen = turtle.Screen()
screen.bgcolor("#050505")
# We removed screen.tracer(0) so you can see it happen live

t = turtle.Turtle()
t.hideturtle()
t.speed(0) # '0' is fastest, but turtle still draws line by line

def draw_creeping_vein(x, y, size, depth):
    if depth == 0:
        return
    
    # Blood-red to necrotic black
    colors = ["#4a0000", "#2b0000", "#120000", "#31004a"]
    t.pencolor(random.choice(colors))
    
    t.penup()
    t.goto(x, y)
    t.pendown()
    
    # Thicker at the start, thin/needle-like at the ends
    t.pensize(depth // 2 + 1)
    
    # The 'Crawl': Small, erratic steps
    new_x = x + random.uniform(-size, size)
    new_y = y + random.uniform(-size, size)
    
    t.goto(new_x, new_y)
    
    # This creates the "branching out" effect
    for _ in range(random.randint(1, 2)):
        draw_creeping_vein(new_x, new_y, size * 0.85, depth - 1)

# This loop makes it start in different spots, one after another
for _ in range(3):
    start_x = random.randint(-100, 100)
    start_y = random.randint(-100, 100)
    draw_creeping_vein(start_x, start_y, 60, 7)

turtle.done()