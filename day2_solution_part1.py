# Find invalid product IDs (numbers that are a pattern repeated twice)
"""
The Core Lesson:
Pattern matching and string manipulation - recognizing that numbers can be treated as strings 
to find structural patterns (like palindromes, repeated sequences, etc.)

1. String Manipulation & Pattern Recognition

Converting numbers to strings to analyze their structure

Splitting strings in half

Comparing patterns

2. String Slicing

s[:half] - first half of string

s[half:] - second half of string

3. Even/Odd Logic

length % 2 == 0 - checking if a number has even length

Only even-length numbers can be split into two identical halves

4. Range Processing

Parsing ranges like "11-22"

Iterating through large number ranges efficiently

5. Problem Optimization (Important!)

Some ranges are HUGE (like 9957459726-9957683116 - over 200,000 numbers!)

The puzzle teaches you to think about performance

Brute force works but might be slow for very large ranges

In real scenarios, you'd optimize by calculating which numbers in a range match the pattern instead of checking every single one
"""

def is_invalid(num):
    s = str(num)
    length = len(s)
    if length % 2 == 0:
        half = length // 2
        if s[:half] == s[half:]:
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
