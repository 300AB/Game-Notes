import pygame
import math

# Node visual base size
r = 12

# Node type colors
node_colors = {
    "grace": (250, 250, 210),
    "foe_drop": (200, 0, 0),
    "boss": (150, 0, 0),
    "loot_pickup": (160, 32, 240),
    "location_note": (180, 180, 180),
    "deathroot": (100, 100, 100),
    "dungeon": (255, 160, 100),
    "evergoal": (100, 180, 255)
}

# === Shape functions ===
def draw_star(surface, color, center, size):
    points = []
    angle = math.pi / 2
    for i in range(10):
        radius = size if i % 2 == 0 else size / 2.5
        x = center[0] + math.cos(angle) * radius
        y = center[1] - math.sin(angle) * radius
        points.append((x, y))
        angle += math.pi / 5
    pygame.draw.polygon(surface, color, points)

def draw_square(surface, color, center, size):
    half = size / 2
    rect = pygame.Rect(center[0] - half, center[1] - half, size, size)
    pygame.draw.rect(surface, color, rect)

def draw_diamond(surface, color, center, size):
    half = size / 2
    points = [
        (center[0], center[1] - half),
        (center[0] + half, center[1]),
        (center[0], center[1] + half),
        (center[0] - half, center[1]),
    ]
    pygame.draw.polygon(surface, color, points)

def draw_circle(surface, color, center, size):
    pygame.draw.circle(surface, color, center, int(size / 2))

def draw_hexagon(surface, color, center, size):
    points = []
    for i in range(6):
        angle = math.pi / 3 * i
        x = center[0] + math.cos(angle) * size
        y = center[1] + math.sin(angle) * size
        points.append((x, y))
    pygame.draw.polygon(surface, color, points)

def draw_triangle(surface, color, center, size):
    half = size / 2
    height = half * math.sqrt(3)
    points = [
        (center[0], center[1] - 2/3 * height),
        (center[0] - half, center[1] + 1/3 * height),
        (center[0] + half, center[1] + 1/3 * height),
    ]
    pygame.draw.polygon(surface, color, points)

# === Unified node renderer ===
def draw_node(surface, node, color, pos):
    size = r
    node_type = node.get("type", "location_note")

    if node_type == "grace":
        draw_triangle(surface, color, pos, size * 2)
    elif node_type == "foe_drop":
        draw_star(surface, color, pos, size * 1.2)
    elif node_type == "loot_pickup":
        draw_diamond(surface, color, pos, size * 1.5)
    elif node_type == "location_note":
        draw_circle(surface, color, pos, size * 1.5)
    elif node_type == "boss":
        draw_hexagon(surface, color, pos, size * 1.2)
    elif node_type == "deathroot":
        draw_diamond(surface, color, pos, size * 1.5)
    elif node_type == "dungeon":
        draw_square(surface, color, pos, size * 1.6)
    elif node_type == "evergoal":
        draw_hexagon(surface, color, pos, size * 1.4)
    else:
        draw_circle(surface, color, pos, size)

# === Label drawing ===
def draw_label(surface, text, pos, font, fg_color, bg_color, padding):
    text_surface = font.render(text, True, fg_color)
    w, h = text_surface.get_size()
    label_rect = pygame.Rect(pos[0] - w // 2 - padding, pos[1] - h // 2 - padding,
                             w + padding * 2, h + padding * 2)
    pygame.draw.rect(surface, bg_color, label_rect)
    surface.blit(text_surface, (label_rect.x + padding, label_rect.y + padding))
