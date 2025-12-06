# Find invalid product IDs (numbers that are a pattern repeated 2+ times)

def is_invalid(num):
    s = str(num)
    length = len(s)
    
    # Try all possible pattern lengths (from 1 to half the string length)
    for pattern_len in range(1, length // 2 + 1):
        if length % pattern_len == 0:  # Length must be divisible by pattern length
            pattern = s[:pattern_len]
            # Check if the entire string is this pattern repeated
            if pattern * (length // pattern_len) == s:
                return True
    return False

total = 0

with open('2_day.txt') as file:
    data = file.read().strip()
    ranges = data.split(',')
    
    for r in ranges:
        start, end = map(int, r.split('-'))
        for num in range(start, end + 1):
            if is_invalid(num):
                total += num

print(total)
