f = open("9_day.txt", "r")
input_str = f.read().split("\n")
f.close()

points = []
for line in input_str:
    if line.strip():
        x, y = line.split(",")
        points.append((int(x), int(y)))

def get_direction(point1, point2):
    if point1[0] == point2[0]:
        if point1[1] < point2[1]:
            return "DOWN"
        else:
            return "UP"
    else:
        if point1[0] < point2[0]:
            return "RIGHT"
        else:
            return "LEFT"

outer_edge = set([])
edges = set()
for i in range(len(points)):
    point1, point2 = points[i], points[(i + 1) % len(points)]
    p1_x, p1_y = points[i]
    p2_x, p2_y = points[(i + 1) % len(points)]

    direction = get_direction(point1, point2)
    dy = abs(point1[1] - point2[1])
    dx = abs(point1[0] - point2[0])
    if direction == "UP":
        start_x, start_y = p1_x, max(p1_y, p2_y)
        for _ in range(dy + 1):
            outer_edge.add((start_x - 1, start_y))
            edges.add((start_x, start_y))
            start_y -= 1
    elif direction == "RIGHT":
        start_x, start_y = min(p1_x, p2_x), p1_y
        for _ in range(dx + 1):
            outer_edge.add((start_x, start_y - 1))
            edges.add((start_x, start_y))
            start_x += 1
    elif direction == "DOWN":
        start_x, start_y = p1_x, min(p1_y, p2_y)
        for _ in range(dy + 1):
            outer_edge.add((start_x + 1, start_y))
            edges.add((start_x, start_y))
            start_y += 1
    else:
        start_x, start_y = max(p1_x, p2_x), p1_y
        for _ in range(dx + 1):
            outer_edge.add((start_x, start_y + 1))
            edges.add((start_x, start_y))
            start_x -= 1

for (x, y) in edges:
    if (x, y) in outer_edge:
        outer_edge.remove((x, y))

def rectangle_size(point_x, point_y):
    dx = abs(point_x[0] - point_y[0]) + 1
    dy = abs(point_x[1] - point_y[1]) + 1
    return dx * dy

def check_rectangle(point_x, point_y):
    r1, c1 = point_x
    r2, c2 = point_y
    
    min_r, max_r = min(r1, r2), max(r1, r2)
    min_c, max_c = min(c1, c2), max(c1, c2)
    
    for c in range(min_c, max_c + 1):
        if (min_r, c) in outer_edge:
            return False
    
    for r in range(min_r + 1, max_r + 1):
        if (r, max_c) in outer_edge:
            return False
    
    for c in range(max_c - 1, min_c - 1, -1):
        if (max_r, c) in outer_edge:
            return False
    
    for r in range(max_r - 1, min_r, -1):
        if (r, min_c) in outer_edge:
            return False
    
    return True

max_size = 0
for i in range(len(points)):
    for j in range(i + 1, len(points)):
        if check_rectangle(points[i], points[j]):
            max_size = max(max_size, rectangle_size(points[i], points[j]))

print(max_size)