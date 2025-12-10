def parse_machine(line):
    parts = line.strip().split('] ')
    target_str = parts[0][1:]
    target = [1 if c == '#' else 0 for c in target_str]
    
    button_part = parts[1].split('{')[0].strip()
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
    
    return target, buttons

def solve_machine_gf2(target, buttons):
    n_lights = len(target)
    n_buttons = len(buttons)
    
    # Create augmented matrix
    matrix = []
    for light in range(n_lights):
        row = [0] * (n_buttons + 1)
        for button_idx, button_lights in enumerate(buttons):
            if light in button_lights:
                row[button_idx] = 1
        row[n_buttons] = target[light]
        matrix.append(row)
    
    # Gaussian elimination
    pivot_cols = []
    current_row = 0
    
    for col in range(n_buttons):
        pivot_row = None
        for row in range(current_row, n_lights):
            if matrix[row][col] == 1:
                pivot_row = row
                break
        
        if pivot_row is None:
            continue
        
        if pivot_row != current_row:
            matrix[current_row], matrix[pivot_row] = matrix[pivot_row], matrix[current_row]
        
        pivot_cols.append(col)
        
        for row in range(n_lights):
            if row != current_row and matrix[row][col] == 1:
                for c in range(n_buttons + 1):
                    matrix[row][c] ^= matrix[current_row][c]
        
        current_row += 1
    
    # Check for inconsistency
    for row in range(current_row, n_lights):
        if matrix[row][n_buttons] == 1:
            return float('inf')
    
    # Find free variables
    free_vars = [i for i in range(n_buttons) if i not in pivot_cols]
    
    # Try all combinations
    min_presses = float('inf')
    
    for mask in range(1 << len(free_vars)):
        solution = [0] * n_buttons
        for i, var_idx in enumerate(free_vars):
            solution[var_idx] = (mask >> i) & 1
        
        # Back-substitution
        for i in range(len(pivot_cols) - 1, -1, -1):
            col = pivot_cols[i]
            val = matrix[i][n_buttons]
            for j in range(col + 1, n_buttons):
                if matrix[i][j] == 1 and solution[j] == 1:
                    val ^= 1
            solution[col] = val
        
        min_presses = min(min_presses, sum(solution))
    
    return min_presses

total = 0
with open('10_day.txt') as f:
    for line in f:
        if line.strip():
            target, buttons = parse_machine(line)
            total += solve_machine_gf2(target, buttons)

print(total)