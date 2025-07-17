import pygame
import json
import os
import math

# === Config & Colors ===
NODE_RADIUS = 12
MIN_DISTANCE = NODE_RADIUS * 2 + 6  # minimal gap between centers (with some padding)
LABEL_FG = (70, 110, 40)
LABEL_BG = (8, 20, 8)
LABEL_PADDING = 6

BG_COLOR = (10, 10, 10)
GRID_COLOR = (100, 100, 100)

PADDING = 40  # pixel padding around bounding box

# Node colors by type
node_colors = {
    "grace": (250, 250, 210),
    "foe_drop": (200, 0, 0),
    "boss": (150, 0, 0),
    "mini_boss": (180, 50, 50),
    "main_boss": (220, 20, 20),
    "event_boss": (255, 100, 100),
    "loot_pickup": (160, 32, 240),
    "location_note": (180, 180, 180),
    "deathroot": (100, 100, 100),
    "dungeon": (255, 160, 100),
    "evergoal": (100, 180, 255),
}

pygame.init()
font = pygame.font.SysFont("Comic Neue", 16)

# Load map data
json_path = os.path.join(os.path.dirname(__file__), "map_data.json")
with open(json_path) as f:
    data = json.load(f)

nodes_raw = data["nodes"]
paths = data["paths"]
bosses = data.get("bosses", {})

# Compute bounding box of raw positions including bosses
all_x = [node["pos"][0] for node in nodes_raw.values()] + [boss["pos"][0] for boss in bosses.values()]
all_y = [node["pos"][1] for node in nodes_raw.values()] + [boss["pos"][1] for boss in bosses.values()]
min_x, max_x = min(all_x), max(all_x)
min_y, max_y = min(all_y), max(all_y)

# Canvas size with padding
width = max_x - min_x + PADDING * 2
height = max_y - min_y + PADDING * 2

# Offset all positions to fit inside padded window
offset_x = min_x - PADDING
offset_y = min_y - PADDING

# Prepare nodes with offset positions
nodes = {}
for key, node in nodes_raw.items():
    x, y = node["pos"]
    nodes[key] = {**node, "pos": [x - offset_x, y - offset_y]}  # mutable list for position

# Add bosses as nodes with offset positions
for key, boss in bosses.items():
    x, y = boss["pos"]
    nodes[key] = {
        "name": boss.get("name", key),
        "pos": [x - offset_x, y - offset_y],
        "type": boss.get("type", "boss"),
    }

# Function: resolve overlaps by pushing nodes apart
def resolve_overlaps(nodes_dict, iterations=100):
    keys = list(nodes_dict.keys())
    for _ in range(iterations):
        moved = False
        for i in range(len(keys)):
            for j in range(i + 1, len(keys)):
                node_a = nodes_dict[keys[i]]
                node_b = nodes_dict[keys[j]]
                ax, ay = node_a["pos"]
                bx, by = node_b["pos"]

                dx = bx - ax
                dy = by - ay
                dist = math.hypot(dx, dy)
                if dist == 0:
                    dx, dy = 1, 1
                    dist = math.hypot(dx, dy)

                if dist < MIN_DISTANCE:
                    overlap = MIN_DISTANCE - dist
                    nx = dx / dist
                    ny = dy / dist
                    shift_x = nx * (overlap / 2)
                    shift_y = ny * (overlap / 2)

                    node_a["pos"][0] -= shift_x
                    node_a["pos"][1] -= shift_y
                    node_b["pos"][0] += shift_x
                    node_b["pos"][1] += shift_y
                    moved = True
        if not moved:
            break

resolve_overlaps(nodes)

screen = pygame.display.set_mode((int(width), int(height)))
pygame.display.set_caption("Bloodice Elden Ring Map")

GRID_SIZE = 64
def draw_grid(surface):
    cols = width // GRID_SIZE + 2
    rows = height // GRID_SIZE + 2
    for c in range(cols):
        x = c * GRID_SIZE
        pygame.draw.line(surface, GRID_COLOR, (x, 0), (x, height))
    for r in range(rows):
        y = r * GRID_SIZE
        pygame.draw.line(surface, GRID_COLOR, (0, y), (width, y))

def draw_label(surface, text, pos, font, fg_color, bg_color, padding):
    text_surf = font.render(text, True, fg_color)
    text_rect = text_surf.get_rect(center=pos)
    bg_rect = text_rect.inflate(padding * 2, padding * 2)
    pygame.draw.rect(surface, bg_color, bg_rect, border_radius=4)
    surface.blit(text_surf, text_rect)

def draw_path(surface, pos1, pos2, color=(150, 150, 150)):
    pygame.draw.line(surface, color, pos1, pos2, width=3)

running = True
clock = pygame.time.Clock()
hover_label = None
hover_pos = None

while running:
    clock.tick(30)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(BG_COLOR)
    draw_grid(screen)

    # Draw paths
    for start_key, end_key in paths:
        if start_key in nodes and end_key in nodes:
            draw_path(screen, nodes[start_key]["pos"], nodes[end_key]["pos"])

    hover_label = None
    hover_pos = None

    mouse_pos = pygame.mouse.get_pos()

    # Draw nodes & check hover
    for node in nodes.values():
        px, py = node["pos"]
        color = node_colors.get(node.get("type"), (200, 200, 200))
        pygame.draw.circle(screen, color, (int(px), int(py)), NODE_RADIUS)

        rect = pygame.Rect(px - NODE_RADIUS, py - NODE_RADIUS, NODE_RADIUS * 2, NODE_RADIUS * 2)
        if rect.collidepoint(mouse_pos):
            hover_label = node["name"]
            hover_pos = (px, py - NODE_RADIUS - 10)

    if hover_label:
        draw_label(screen, hover_label, hover_pos, font,
                   fg_color=LABEL_FG, bg_color=LABEL_BG, padding=LABEL_PADDING)

    pygame.display.flip()

pygame.quit()
