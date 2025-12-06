# Count how many times the dial points to 0
position = 50
zero_count = 0

with open('1_day.txt') as file:
    for line in file:
        line = line.strip() # removes whitespace characters (spaces, tabs, newlines) from both the beginning and end of the string.
        if not line:
            continue
            
        direction = line[0] # get the rotation direction data
        distance = int(line[1:]) # gets all characters from index 1 to the end (everything except the first character), then int() converts it to an integer. it is set at one as ) is the Lettre

        
        if direction == 'L':
            position = (position - distance) % 100 # the % modulo operator gives us the remainder in relation tot he wrap arounrd and 100 is becuase there are 0-99 options
        else:
            position = (position + distance) % 100
        
        if position == 0:
            zero_count += 1

print(zero_count)
