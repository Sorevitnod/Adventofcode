# Parse input
tiles = []
with open('9_day.txt') as f:
    for line in f:
        line = line.strip()
        if line:
            x, y = map(int, line.split(','))
            tiles.append((x, y))

n = len(tiles)

# Point in polygon test
def point_in_polygon(px, py):
    inside = False
    j = n - 1
    for i in range(n):
        xi, yi = tiles[i]
        xj, yj = tiles[j]
        if ((yi > py) != (yj > py)) and (px < (xj - xi) * (py - yi) / (yj - yi) + xi):
            inside = not inside
        j = i
    return inside

# Check if point is on polygon edge
def on_edge(px, py):
    for i in range(n):
        x1, y1 = tiles[i]
        x2, y2 = tiles[(i + 1) % n]
        
        if x1 == x2 == px:
            if min(y1, y2) <= py <= max(y1, y2):
                return True
        elif y1 == y2 == py:
            if min(x1, x2) <= px <= max(x1, x2):
                return True
    return False

# Check if point is valid (inside or on edge)
def is_valid(px, py):
    return on_edge(px, py) or point_in_polygon(px, py)

# Find largest rectangle
max_area = 0
for i in range(n):
    for j in range(i + 1, n):
        x1, y1 = tiles[i]
        x2, y2 = tiles[j]
        
        # Check all 4 corners
        if is_valid(x1, y1) and is_valid(x2, y2) and is_valid(x1, y2) and is_valid(x2, y1):
            area = abs(x2 - x1) * abs(y2 - y1)
            max_area = max(max_area, area)

print(max_area)
