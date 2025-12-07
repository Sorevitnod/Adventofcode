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

# Track paths: each path is a tuple of column positions at each row
paths = [(start_col,)]

# Process each row
for row in range(1, len(grid)):
    new_paths = []
    
    for path in paths:
        col = path[-1]  # Current column position
        
        if 0 <= col < len(grid[row]):
            if grid[row][col] == '^':
                # Split: create two paths (left and right)
                if col - 1 >= 0:
                    new_paths.append(path + (col - 1,))
                if col + 1 < len(grid[row]):
                    new_paths.append(path + (col + 1,))
            else:
                # Continue straight
                new_paths.append(path + (col,))
    
    paths = new_paths

end_time = time.time()

print(len(paths))
print(f"Processing time: {end_time - start_time:.4f} seconds")
