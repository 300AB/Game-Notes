import tkinter as tk

nodes = {
    "Chapel of Anticipation": (50, 300),
    "Bridge Spawn": (120, 320),
    "First Grace": (180, 340),
    "Fractured Peninsula": (240, 380),
    "Cave of Loot X": (300, 420),
    "West Limgrave": (360, 380),
    "Ruined Fort": (440, 320),
    "Bandit Camp": (440, 400),
    "Knight Drop": (500, 360),
    "Swamp Fringe": (580, 320),
    "Caelid Edge": (580, 420)
}

colors = {
    "Chapel of Anticipation": "white",
    "Bridge Spawn": "gray",
    "First Grace": "gray",
    "Fractured Peninsula": "gray",
    "Cave of Loot X": "purple",
    "West Limgrave": "white",
    "Ruined Fort": "blue",
    "Bandit Camp": "red",
    "Knight Drop": "red",
    "Swamp Fringe": "gray",
    "Caelid Edge": "gray"
}

paths = [
    ("Chapel of Anticipation", "Bridge Spawn"),
    ("Bridge Spawn", "First Grace"),
    ("First Grace", "Fractured Peninsula"),
    ("Fractured Peninsula", "Cave of Loot X"),
    ("Fractured Peninsula", "West Limgrave"),
    ("West Limgrave", "Ruined Fort"),
    ("West Limgrave", "Bandit Camp"),
    ("Bandit Camp", "Knight Drop"),
    ("Knight Drop", "Swamp Fringe"),
    ("Knight Drop", "Caelid Edge")
]

# Setup window
root = tk.Tk()
root.title("Bloodice Trail - TK Map")
canvas = tk.Canvas(root, width=800, height=600, bg="black")
canvas.pack()

# Draw lines
for a, b in paths:
    x1, y1 = nodes[a]
    x2, y2 = nodes[b]
    canvas.create_line(x1, y1, x2, y2, fill="white", dash=(5, 5))

# Draw nodes and labels
for name, (x, y) in nodes.items():
    color = colors.get(name, "white")
    canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill=color, outline="")
    canvas.create_text(x + 10, y - 10, anchor="nw", text=name, fill="white", font=("Courier", 9))

root.mainloop()
