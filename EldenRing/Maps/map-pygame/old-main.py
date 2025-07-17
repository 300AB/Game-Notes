import pygame
import json
import os
from shapes import draw_node, draw_label, node_colors
from grid import to_grid_center, find_free_cell, GRID_SIZE, GRID_OFFSET
from path import draw_path

LABEL_FG = (70, 110, 40)
LABEL_BG = (8, 20, 8)
LABEL_PADDING = 6
BG_COLOR = (10, 10, 10)
GRID_COLOR = (100, 100, 100)

# Load data
json_path = os.path.join(os.path.dirname(__file__), "nodes_paths.json")
with open(json_path) as f:
    data = json.load(f)
nodes_raw = data["nodes"]
paths = data["paths"]

# Place nodes in grid
taken_cells = set()
nodes = {}
for key, node in nodes_raw.items():
    desired = to_grid_center(node["pos"])
    free = find_free_cell(taken_cells, desired)
    taken_cells.add(free)
    nodes[key] = {**node, "pos": free}

# Compute grid bounds (with 2-cell buffer)
all_x = [n["pos"][0] for n in nodes.values()]
all_y = [n["pos"][1] for n in nodes.values()]
min_x, max_x = min(all_x), max(all_x)
min_y, max_y = min(all_y), max(all_y)

min_grid_x = ((min_x - GRID_OFFSET[0]) // GRID_SIZE) - 2
max_grid_x = ((max_x - GRID_OFFSET[0]) // GRID_SIZE) + 2
min_grid_y = ((min_y - GRID_OFFSET[1]) // GRID_SIZE) - 2
max_grid_y = ((max_y - GRID_OFFSET[1]) // GRID_SIZE) + 2

grid_pixel_min_x = GRID_OFFSET[0] + min_grid_x * GRID_SIZE
grid_pixel_max_x = GRID_OFFSET[0] + (max_grid_x + 1) * GRID_SIZE
grid_pixel_min_y = GRID_OFFSET[1] + min_grid_y * GRID_SIZE
grid_pixel_max_y = GRID_OFFSET[1] + (max_grid_y + 1) * GRID_SIZE

canvas_width = grid_pixel_max_x - grid_pixel_min_x
canvas_height = grid_pixel_max_y - grid_pixel_min_y

pygame.init()
screen = pygame.display.set_mode((canvas_width, canvas_height))
pygame.display.set_caption("Bloodice Elden Ring Map")
font = pygame.font.SysFont("Comic Neue", 16)

def draw_grid(surface):
    for gx in range(min_grid_x, max_grid_x + 1):
        x = GRID_OFFSET[0] + gx * GRID_SIZE - grid_pixel_min_x
        pygame.draw.line(surface, GRID_COLOR, (x, 0), (x, canvas_height))
    for gy in range(min_grid_y, max_grid_y + 1):
        y = GRID_OFFSET[1] + gy * GRID_SIZE - grid_pixel_min_y
        pygame.draw.line(surface, GRID_COLOR, (0, y), (canvas_width, y))

running = True
clock = pygame.time.Clock()

while running:
    clock.tick(30)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(BG_COLOR)

    draw_grid(screen)

    # Draw paths behind nodes
    for p1, p2 in paths:
        if p1 in nodes and p2 in nodes:
            a = nodes[p1]["pos"]
            b = nodes[p2]["pos"]
            offset_a = (a[0] - grid_pixel_min_x, a[1] - grid_pixel_min_y)
            offset_b = (b[0] - grid_pixel_min_x, b[1] - grid_pixel_min_y)
            draw_path(screen, offset_a, offset_b)

    hover_label = None
    hover_pos = None

    # Draw nodes
    for node in nodes.values():
        raw_pos = node["pos"]
        pos = (raw_pos[0] - grid_pixel_min_x, raw_pos[1] - grid_pixel_min_y)
        node_type = node.get("type", "location_note")
        color = node_colors.get(node_type)

        if not color or not (isinstance(color, (tuple, list)) and len(color) in (3, 4)):
            color = (255, 255, 255)  # fallback white

        draw_node(screen, node, pos, color)

        # Hover check
        box = pygame.Rect(pos[0] - 15, pos[1] - 15, 30, 30)
        if box.collidepoint(pygame.mouse.get_pos()):
            hover_label = node["name"]
            hover_pos = (pos[0], pos[1] - 20)

    if hover_label:
        draw_label(screen, hover_label, hover_pos, font, fg_color=LABEL_FG, bg_color=LABEL_BG, padding=LABEL_PADDING)

    pygame.display.flip()

pygame.quit()
