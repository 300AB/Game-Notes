import pygame

PATH_COLOR = (70, 110, 40)
PATH_WIDTH = 3

def draw_path(surface, start_pos, end_pos, color=PATH_COLOR):
    pygame.draw.line(surface, color, start_pos, end_pos, PATH_WIDTH)
