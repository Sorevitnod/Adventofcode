position = 50
count = 0

with open('1_day.txt') as f:
    for line in f:
        line = line.strip()
        if line:
            direction = line[0]
            distance = int(line[1:])
            position = (position - distance) % 100 if direction == 'L' else (position + distance) % 100
            if position == 0:
                count += 1

print(count)
