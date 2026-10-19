"""Maze loading.

A maze is a text file where
    #  wall
    A  start
    B  goal
    anything else is free space
Rows may have different lengths; missing cells count as walls.
"""

from typing import List, Tuple

Cell = Tuple[int, int]  # (row, col)

# (dr, dc) for right, down, up, left - the same order as the original script
MOVES = [(0, 1), (1, 0), (-1, 0), (0, -1)]


class Maze:
    def __init__(self, rows: List[str]):
        rows = [r.rstrip("\n") for r in rows]
        while rows and not rows[-1].strip():
            rows.pop()
        self.height = len(rows)
        self.width = max(len(r) for r in rows)
        self.grid = [list(r.ljust(self.width, "#")) for r in rows]

        self.start = self._find("A")
        self.goal = self._find("B")

    @classmethod
    def from_file(cls, path: str) -> "Maze":
        with open(path) as f:
            return cls(f.readlines())

    def _find(self, ch: str) -> Cell:
        for r, row in enumerate(self.grid):
            for c, v in enumerate(row):
                if v == ch:
                    return (r, c)
        raise ValueError(f"maze has no '{ch}'")

    def is_wall(self, cell: Cell) -> bool:
        r, c = cell
        if not (0 <= r < self.height and 0 <= c < self.width):
            return True
        return self.grid[r][c] == "#"

    def neighbours(self, cell: Cell) -> List[Tuple[Cell, Tuple[int, int]]]:
        out = []
        for dr, dc in MOVES:
            nxt = (cell[0] + dr, cell[1] + dc)
            if not self.is_wall(nxt):
                out.append((nxt, (dr, dc)))
        return out

    def __str__(self) -> str:
        return "\n".join("".join(r) for r in self.grid)
