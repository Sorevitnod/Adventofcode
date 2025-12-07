# Count how many times the tachyon beam is split

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

# Track active beams: list of (row, col) positions
beams = [start_col]
split_count = 0

# Process each row
for row in range(1, len(grid)):
    new_beams = []
    
    for col in beams:
        if 0 <= col < len(grid[row]):
            if grid[row][col] == '^':
                # Split: add left and right positions
                split_count += 1
                if col - 1 >= 0:
                    new_beams.append(col - 1)
                if col + 1 < len(grid[row]):
                    new_beams.append(col + 1)
            else:
                # Continue straight down
                new_beams.append(col)
    
    # Remove duplicates (beams in same column)
    beams = list(set(new_beams))

print(split_count)
