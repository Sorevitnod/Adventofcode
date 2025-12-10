# Parse input
tiles = []
with open('9_day.txt') as f:
    for line in f:
        line = line.strip()
        if line:
            x, y = map(int, line.split(','))
            tiles.append((x, y))

# Find largest rectangle
max_area = 0
n = len(tiles)

for i in range(n):
    for j in range(i + 1, n):
        x1, y1 = tiles[i]
        x2, y2 = tiles[j]
        
        # Calculate area
        width = abs(x2 - x1)
        height = abs(y2 - y1)
        area = width * height
        
        max_area = max(max_area, area)

print(max_area)
