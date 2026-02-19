from turtle import *

# Setup the window
setup(600, 600)
bgcolor("white")
speed(3)
penup()

# Logo configuration
logo_blue = "#0078d4"  # Official Microsoft Blue
size = 100             # Size of each pane
gap = 10               # Space between panes

def draw_pane(x, y, color):
    """Draws a single square pane of the logo"""
    goto(x, y)
    setheading(0)
    fillcolor(color)
    begin_fill()
    for _ in range(4):
        forward(size)
        left(90)
    end_fill()

# Draw the 4 panes
hideturtle()

# Top Left
draw_pane(-size - gap/2, gap/2, logo_blue)

# Top Right
draw_pane(gap/2, gap/2, logo_blue)

# Bottom Left
draw_pane(-size - gap/2, -size - gap/2, logo_blue)

# Bottom Right
draw_pane(gap/2, -size - gap/2, logo_blue)

done()