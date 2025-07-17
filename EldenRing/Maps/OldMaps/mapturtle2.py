import turtle

screen = turtle.Screen()
screen.title("Bloodice Grave-Robbery Trail v2")
screen.bgcolor("black")

pen = turtle.Turtle()
pen.speed(0)
pen.color("white")
pen.penup()

nodes = {
    "Chapel of Anticipation": (-300, 0),
    "Bridge Spawn": (-240, -20),
    "First Grace (Stranded Graveyard)": (-200, -40),
    "Fractured Peninsula": (-160, -80),
    "Cave of Loot X": (-100, -120),
    "Mainland (West Limgrave)": (-40, -80),
    "Ruined Fort (Fashion Armor)": (40, -20),
    "Bandit Camp (Dex Bloodice)": (40, -100),
    "Knight Drop Zone (Heavy Bloodice)": (100, -60),
    "Fringe Swamp (School Border)": (160, -20),
    "Caelid Edge": (160, -120)
}

loot_type = {
    "Chapel of Anticipation": "white",
    "Bridge Spawn": "gray",
    "First Grace": "gray",
    "Fractured Peninsula": "gray",
    "Cave of Loot X": "purple",
    "Mainland (West Limgrave)": "white",
    "Ruined Fort (Fashion Armor)": "blue",
    "Bandit Camp (Dex Bloodice)": "red",
    "Knight Drop Zone (Heavy Bloodice)": "red",
    "Fringe Swamp (School Border)": "gray",
    "Caelid Edge": "gray"
}

graces = {
    "Cave of Loot X": "Seaside Ruins",
    "Ruined Fort (Fashion Armor)": "Mistwood Outskirts",
    "Bandit Camp (Dex Bloodice)": "Agheel Lake North",
    "Knight Drop Zone (Heavy Bloodice)": "Waypoint Ruins Cellar",
    "Fringe Swamp (School Border)": "South Raya Lucaria Gate",
    "Caelid Edge": "Smoldering Wall"
}

# Draw all nodes and labels
for name, (x, y) in nodes.items():
    color = loot_type.get(name, "white")
    pen.goto(x, y)
    pen.dot(12, color)
    pen.goto(x + 8, y + 8)
    pen.write(name, font=("Courier", 9, "normal"))
    if name in graces:
        pen.goto(x + 8, y - 12)
        pen.color("light green")
        pen.write(f"Grace: {graces[name]}", font=("Courier", 8, "italic"))
        pen.color("white")

def dotted_path(a, b):
    pen.goto(*nodes[a])
    pen.setheading(pen.towards(*nodes[b]))
    dist = pen.distance(*nodes[b])
    steps = int(dist // 15)
    pen.pendown()
    for _ in range(steps):
        pen.forward(10)
        pen.penup()
        pen.forward(5)
        pen.pendown()
    pen.penup()

# Path network
paths = [
    ("Chapel of Anticipation", "Bridge Spawn"),
    ("Bridge Spawn", "First Grace (Stranded Graveyard)"),
    ("First Grace (Stranded Graveyard)", "Fractured Peninsula"),
    ("Fractured Peninsula", "Cave of Loot X"),
    ("Fractured Peninsula", "Mainland (West Limgrave)"),
    ("Mainland (West Limgrave)", "Ruined Fort (Fashion Armor)"),
    ("Mainland (West Limgrave)", "Bandit Camp (Dex Bloodice)"),
    ("Bandit Camp (Dex Bloodice)", "Knight Drop Zone (Heavy Bloodice)"),
    ("Knight Drop Zone (Heavy Bloodice)", "Fringe Swamp (School Border)"),
    ("Knight Drop Zone (Heavy Bloodice)", "Caelid Edge")
]

for a, b in paths:
    dotted_path(a, b)

pen.hideturtle()
turtle.done()
