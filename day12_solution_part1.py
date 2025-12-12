import sys
from typing import List, Tuple, Optional

# Polyomino representation: list of strings, '#' for filled, '.' for empty
Poly = List[str]

# All possible orientations (rotations and flips)
def get_all_variants(poly: Poly) -> List[Poly]:
    variants = []
    current = poly
    for flip in [False, True]:
        if flip:
            current = [row[::-1] for row in current]
        p = current
        for _ in range(4):
            variants.append(p)
            # Rotate 90 clockwise
            h = len(p)
            w = len(p[0])
            p = [''.join(p[r][c] for r in range(h-1, -1, -1)) for c in range(w)]
    return variants

Position = Tuple[int, int]
Piece = List[Position]  # relative positions, top-left is (0,0), min r,c =0

def get_positions(poly: Poly) -> Piece:
    positions = []
    for r in range(len(poly)):
        for c in range(len(poly[r])):
            if poly[r][c] == '#':
                positions.append((r, c))
    if positions:
        min_r = min(pr for pr, pc in positions)
        min_c = min(pc for pr, pc in positions)
        positions = [(pr - min_r, pc - min_c) for pr, pc in positions]
    return positions

def precompute_pieces(shapes: List[Poly]) -> List[List[Piece]]:
    all_pieces = []
    for poly in shapes:
        variants = get_all_variants(poly)
        unique_pieces = []
        seen = set()
        for v in variants:
            pos = tuple(sorted(get_positions(v)))
            if pos not in seen:
                seen.add(pos)
                unique_pieces.append(get_positions(v))
        all_pieces.append(unique_pieces)
    return all_pieces

# Placement: place a piece at row_offset, col_offset on grid
Grid = List[List[bool]]

def can_place(grid: Grid, piece: Piece, r0: int, c0: int, h: int, w: int) -> bool:
    for dr, dc in piece:
        r = r0 + dr
        c = c0 + dc
        if r >= h or c >= w or grid[r][c]:
            return False
    return True

def place(grid: Grid, piece: Piece, r0: int, c0: int, val: bool = True):
    for dr, dc in piece:
        r = r0 + dr
        c = c0 + dc
        grid[r][c] = val

# Backtracking solver
def solve_region(width: int, height: int, counts: List[int], all_pieces: List[List[Piece]]) -> bool:
    h = height
    w = width
    
    # Flatten the list of required pieces, allowing multiples
    required = []
    for idx, cnt in enumerate(counts):
        required.extend([idx] * cnt)

    n = len(required)

    if n == 0:
        return True

    # Precompute max height and width for each piece type
    max_dh = [0] * len(all_pieces)
    max_dw = [0] * len(all_pieces)
    for idx, variants in enumerate(all_pieces):
        for piece in variants:
            if piece:
                dh = max(r for r,c in piece) + 1
                dw = max(c for r,c in piece) + 1
                max_dh[idx] = max(max_dh[idx], dh)
                max_dw[idx] = max(max_dw[idx], dw)

    def backtrack(pos: int, grid: Optional[Grid] = None) -> bool:
        if pos == n:
            return True
        if grid is None:
            grid = [[False] * w for _ in range(h)]

        type_idx = required[pos]

        # Find possible placements for this type
        variants = all_pieces[type_idx]

        # To speed up, find empty cells to try as anchor
        for r0 in range(h - max_dh[type_idx] + 1):
            for c0 in range(w - max_dw[type_idx] + 1):
                for piece in variants:
                    if can_place(grid, piece, r0, c0, h, w):
                        place(grid, piece, r0, c0, True)
                        if backtrack(pos + 1, grid):
                            return True
                        place(grid, piece, r0, c0, False)  # unplace
        return False

    return backtrack(0)

# Main
def main():
    with open('12_day.txt', 'r') as f:
        data = f.read()
    lines = data.splitlines()

    # Parse shapes
    shapes = []
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if not line:
            i += 1
            continue
        if ':' in line and 'x' not in line:
            shape_lines = []
            i += 1
            while i < len(lines) and lines[i].strip() and ':' not in lines[i] and 'x' not in lines[i]:
                shape_lines.append(lines[i].strip())
                i += 1
            shapes.append(shape_lines)
        else:
            break

    print(f"Parsed {len(shapes)} shapes")

    # Parse regions
    regions = []
    while i < len(lines):
        line = lines[i].strip()
        if not line:
            i += 1
            continue
        if 'x' in line and ':' in line:
            parts = line.split(': ')
            dim = parts[0]
            wh, hh = map(int, dim.split('x'))
            cnts = list(map(int, parts[1].split()))
            if len(cnts) < len(shapes):
                cnts += [0] * (len(shapes) - len(cnts))
            regions.append((wh, hh, cnts))
        i += 1

    print(f"Parsed {len(regions)} regions")

    # Precompute pieces
    all_pieces = precompute_pieces(shapes)

    # Count how many can be solved
    count = 0
    for idx, (w, h, cnts) in enumerate(regions):
        result = solve_region(w, h, cnts, all_pieces)
        if result:
            count += 1
        print(f"Region {idx+1}: {'yes' if result else 'no'}")

    print("Total regions that fit:", count)

if __name__ == "__main__":
    main()