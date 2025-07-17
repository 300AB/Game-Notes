GRID_SIZE = 40
GRID_OFFSET = (30, 30)  # pixel offset from top-left corner

def to_grid_center(pos):
    x, y = pos
    gx = GRID_OFFSET[0] + ((x - GRID_OFFSET[0]) // GRID_SIZE) * GRID_SIZE + GRID_SIZE // 2
    gy = GRID_OFFSET[1] + ((y - GRID_OFFSET[1]) // GRID_SIZE) * GRID_SIZE + GRID_SIZE // 2
    return (gx, gy)

def spiral_offsets(max_radius=3):
    offsets = [(0, 0)]
    for r in range(1, max_radius + 1):
        for dx in range(-r, r + 1):
            offsets.append((dx * GRID_SIZE, -r * GRID_SIZE))  # top row
            offsets.append((dx * GRID_SIZE, r * GRID_SIZE))   # bottom row
        for dy in range(-r + 1, r):
            offsets.append((-r * GRID_SIZE, dy * GRID_SIZE))  # left col
            offsets.append((r * GRID_SIZE, dy * GRID_SIZE))   # right col
    seen = set()
    unique = []
    for off in offsets:
        if off not in seen:
            seen.add(off)
            unique.append(off)
    return unique

def find_free_cell(taken, desired):
    if desired not in taken:
        return desired
    for dx, dy in spiral_offsets():
        candidate = (desired[0] + dx, desired[1] + dy)
        if candidate not in taken:
            return candidate
    return desired  # fallback

def grid_bounds(node_positions, padding_cells=2):
    """
    Given list of (x,y) pixel positions, returns grid bounds with padding cells added,
    in terms of grid indices and pixel bounding box.
    """
    xs = [pos[0] for pos in node_positions]
    ys = [pos[1] for pos in node_positions]

    min_x = min(xs)
    max_x = max(xs)
    min_y = min(ys)
    max_y = max(ys)

    from math import floor, ceil

    min_grid_x = floor((min_x - GRID_OFFSET[0]) / GRID_SIZE) - padding_cells
    max_grid_x = ceil((max_x - GRID_OFFSET[0]) / GRID_SIZE) + padding_cells
    min_grid_y = floor((min_y - GRID_OFFSET[1]) / GRID_SIZE) - padding_cells
    max_grid_y = ceil((max_y - GRID_OFFSET[1]) / GRID_SIZE) + padding_cells

    pixel_min_x = GRID_OFFSET[0] + min_grid_x * GRID_SIZE
    pixel_min_y = GRID_OFFSET[1] + min_grid_y * GRID_SIZE
    pixel_max_x = GRID_OFFSET[0] + (max_grid_x + 1) * GRID_SIZE
    pixel_max_y = GRID_OFFSET[1] + (max_grid_y + 1) * GRID_SIZE

    width = pixel_max_x - pixel_min_x
    height = pixel_max_y - pixel_min_y

    return {
        "min_grid_x": min_grid_x,
        "max_grid_x": max_grid_x,
        "min_grid_y": min_grid_y,
        "max_grid_y": max_grid_y,
        "pixel_min_x": pixel_min_x,
        "pixel_min_y": pixel_min_y,
        "pixel_max_x": pixel_max_x,
        "pixel_max_y": pixel_max_y,
        "width": width,
        "height": height,
    }
