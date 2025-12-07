# Count unique timelines (unique paths through the manifold)
import time

start_time = time.time()

grid = []
with open('7_day.txt') as file:
    for line in file:
        line = line.rstrip('\n\r')
        if line:
            grid.append(line)

# Find starting position (S)
start_col = 0
for col in range(len(grid[0])):
    if grid[0][col] == 'S':
        start_col = col
        break

# Track column positions: use dict to count paths at each column
paths = {start_col: 1}

# Process each row
for row in range(1, len(grid)):
    new_paths = {}
    
    for col, count in paths.items():
        if 0 <= col < len(grid[row]):
            if grid[row][col] == '^':
                # Split: paths go left and right
                if col - 1 >= 0:
                    new_paths[col - 1] = new_paths.get(col - 1, 0) + count
                if col + 1 < len(grid[row]):
                    new_paths[col + 1] = new_paths.get(col + 1, 0) + count
            else:
                # Continue straight
                new_paths[col] = new_paths.get(col, 0) + count
    
    paths = new_paths

end_time = time.time()

print(sum(paths.values()))
print(f"Processing time: {end_time - start_time:.4f} seconds")
