import pulp

def parse_machine(line):
    joltage_start = line.rindex('{')
    joltage_end = line.rindex('}')
    joltage_str = line[joltage_start+1:joltage_end]
    joltages = [int(x.strip()) for x in joltage_str.split(',')]
    
    button_part = line.split('{')[0].strip()
    buttons = []
    current = ""
    in_parens = False
    
    for char in button_part:
        if char == '(':
            in_parens = True
            current = ""
        elif char == ')':
            in_parens = False
            if current:
                button = [int(x) for x in current.split(',')]
                buttons.append(button)
        elif in_parens:
            current += char
    
    return joltages, buttons

def solve_part2_pulp(joltages, buttons):
    n_counters = len(joltages)
    n_buttons = len(buttons)
    
    # Create problem
    prob = pulp.LpProblem("ButtonPresses", pulp.LpMinimize)
    
    # Variables: number of times each button is pressed
    x = [pulp.LpVariable(f"x{i}", lowBound=0, cat='Integer') for i in range(n_buttons)]
    
    # Objective: minimize total button presses
    prob += pulp.lpSum(x)
    
    # Constraints: each counter must reach its target
    for counter_idx in range(n_counters):
        affecting_buttons = [i for i, button in enumerate(buttons) if counter_idx in button]
        if affecting_buttons:
            prob += pulp.lpSum([x[i] for i in affecting_buttons]) == joltages[counter_idx]
    
    # Solve
    prob.solve(pulp.PULP_CBC_CMD(msg=0))
    
    if prob.status == pulp.LpStatusOptimal:
        return int(pulp.value(prob.objective))
    return float('inf')

total = 0
with open('10_day.txt') as f:
    for line in f:
        if line.strip():
            joltages, buttons = parse_machine(line)
            result = solve_part2_pulp(joltages, buttons)
            total += result

print(total)