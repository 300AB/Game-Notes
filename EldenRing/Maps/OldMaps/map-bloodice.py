import turtle

# Setup
screen = turtle.Screen()
screen.bgcolor("black")
pen = turtle.Turtle()
pen.color("white")
pen.speed(0)
pen.penup()

# Landmarks
points = {
    "Margit": (-200, -50),
    "Stormveil Castle": (-150, 50),
    "Murkwater Catacomb": (0, -100),
    "Bloodice Camp": (100, 0),
    "Liurnia Entrance": (200, 100)
}

# Draw landmarks
for name, (x, y) in points.items():
    pen.goto(x, y)
    pen.dot(10, "red")
    pen.write(f" {name}", font=("Arial", 10, "normal"))

# Draw paths
paths = [
    ("Margit", "Stormveil Castle"),
    ("Stormveil Castle", "Murkwater Catacomb"),
    ("Murkwater Catacomb", "Bloodice Camp"),
    ("Stormveil Castle", "Liurnia Entrance")
]

pen.color("gray")
pen.width(2)
for a, b in paths:
    pen.goto(points[a])
    pen.pendown()
    pen.goto(points[b])
    pen.penup()

# Done
pen.hideturtle()
turtle.done()




#This draws:

#Your progression arc

#The divergent Bloodice Camp path

#Labels + dots for key zones