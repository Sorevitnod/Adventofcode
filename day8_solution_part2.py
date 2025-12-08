from collections import defaultdict

# Parse input
boxes = []
with open('8_day.txt') as f:
    for line in f:
        line = line.strip()
        if line:
            x, y, z = map(int, line.split(','))
            boxes.append((x, y, z))

n = len(boxes)

# Union-Find
parent = list(range(n))
rank = [0] * n

def find(x):
    if parent[x] != x:
        parent[x] = find(parent[x])
    return parent[x]

def union(x, y):
    rx, ry = find(x), find(y)
    if rx == ry:
        return False
    if rank[rx] < rank[ry]:
        parent[rx] = ry
    elif rank[rx] > rank[ry]:
        parent[ry] = rx
    else:
        parent[ry] = rx
        rank[rx] += 1
    return True

def count_circuits():
    return len(set(find(i) for i in range(n)))

# Calculate all distances
distances = []
for i in range(n):
    for j in range(i + 1, n):
        x1, y1, z1 = boxes[i]
        x2, y2, z2 = boxes[j]
        dist = ((x1-x2)**2 + (y1-y2)**2 + (z1-z2)**2) ** 0.5
        distances.append((dist, i, j))

distances.sort()

# Connect until all in one circuit
for dist, i, j in distances:
    if union(i, j):
        if count_circuits() == 1:
            result = boxes[i][0] * boxes[j][0]
            print(result)
            break
