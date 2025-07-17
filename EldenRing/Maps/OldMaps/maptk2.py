import tkinter as tk

nodes = {
    "1A: Chapel of Anticipation": (50, 300),
    "1B: Bridge Spawn": (120, 320),
    "2A: First Grace": (180, 340),
    "2B: Fractured Peninsula": (240, 380),
    "2C: Cave of Loot X": (300, 420),
    "3A: West Limgrave": (360, 380),
    "3B: Ruined Fort": (440, 320),
    "3C: Bandit Camp": (440, 400),
    "3D: Knight Drop": (500, 360),
    "4A: Swamp Fringe": (580, 320),
    "4B: Caelid Edge": (580, 420)
}

colors = {
    "1A: Chapel of Anticipation": "white",
    "1B: Bridge Spawn": "gray",
    "2A: First Grace": "gray",
    "2B: Fractured Peninsula": "gray",
    "2C: Cave of Loot X": "purple",
    "3A: West Limgrave": "white",
    "3B: Ruined Fort": "blue",
    "3C: Bandit Camp": "red",
    "3D: Knight Drop": "red",
    "4A: Swamp Fringe": "gray",
    "4B: Caelid Edge": "gray"
}

paths = [
    ("1A: Chapel of Anticipation", "1B: Bridge Spawn"),
    ("1B: Bridge Spawn", "2A: First Grace"),
    ("2A: First Grace", "2B: Fractured Peninsula"),
    ("2B: Fractured Peninsula", "2C: Cave of Loot X"),
    ("2B: Fractured Peninsula", "3A: West Limgrave"),
    ("3A: West Limgrave", "3B: Ruined Fort"),
    ("3A: West Limgrave", "3C: Bandit Camp"),
    ("3C: Bandit Camp", "3D: Knight Drop"),
    ("3D: Knight Drop", "4A: Swamp Fringe"),
    ("3D: Knight Drop", "4B: Caelid Edge")
]

root = tk.Tk()
root.title("Bloodice Trail - Full TK Map")
canvas = tk.Canvas(root, width=900, height=600, bg="black")
canvas.pack()

# Draw paths
for a, b in paths:
    x1, y1 = nodes[a]
    x2, y2 = nodes[b]
    canvas.create_line(x1, y1, x2, y2, fill="white", dash=(5, 5))

# Draw points and labels
for name, (x, y) in nodes.items():
    color = colors.get(name, "white")
    index, label = name.split(": ")
    canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill=color, outline="")
    canvas.create_text(x - 10, y - 18, anchor="nw", text=index, fill="cyan", font=("Courier", 9, "bold"))
    canvas.create_text(x + 8, y + 6, anchor="nw", text=label, fill="white", font=("Courier", 9))

root.mainloop()
