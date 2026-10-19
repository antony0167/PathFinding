"""Random maze generator (recursive backtracker / randomized DFS).

The result is a "perfect" maze: exactly one path between any two cells.
`loops` knocks down extra walls afterwards so there are several routes,
which is where BFS, Greedy and A* start behaving differently.
"""

import random
from typing import List


def generate(rows: int, cols: int, loops: float = 0.08, seed=None) -> List[str]:
    rng = random.Random(seed)
    h, w = 2 * rows + 1, 2 * cols + 1
    grid = [["#"] * w for _ in range(h)]

    stack = [(0, 0)]
    seen = {(0, 0)}
    grid[1][1] = " "
    while stack:
        r, c = stack[-1]
        options = [(r + dr, c + dc) for dr, dc in ((0, 1), (1, 0), (0, -1), (-1, 0))
                   if 0 <= r + dr < rows and 0 <= c + dc < cols and (r + dr, c + dc) not in seen]
        if not options:
            stack.pop()
            continue
        nr, nc = rng.choice(options)
        grid[2 * nr + 1][2 * nc + 1] = " "
        grid[r + nr + 1][c + nc + 1] = " "  # wall between the two cells
        seen.add((nr, nc))
        stack.append((nr, nc))

    # open some extra walls to create loops
    for r in range(1, h - 1):
        for c in range(1, w - 1):
            if grid[r][c] == "#" and rng.random() < loops:
                horiz = grid[r][c - 1] == " " and grid[r][c + 1] == " "
                vert = grid[r - 1][c] == " " and grid[r + 1][c] == " "
                if horiz != vert:
                    grid[r][c] = " "

    grid[h - 2][1] = "A"       # bottom-left
    grid[1][w - 2] = "B"       # top-right
    return ["".join(row) for row in grid]
