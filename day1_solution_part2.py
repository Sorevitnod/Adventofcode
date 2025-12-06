# Count how many times the dial points to 0 or goes past it(including during rotations)
position = 50
zero_count = 0

with open('1_day.txt') as file:
    for line in file:
        line = line.strip()
        if not line:
            continue
            
        direction = line[0]
        distance = int(line[1:])
        
        # Count how many times we pass through 0 during the rotation
        if direction == 'L':
            # Moving left (decreasing)
            for _ in range(distance):
                position = (position - 1) % 100
                if position == 0:
                    zero_count += 1
        else:
            # Moving right (increasing)
            for _ in range(distance):
                position = (position + 1) % 100
                if position == 0:
                    zero_count += 1

print(zero_count)
