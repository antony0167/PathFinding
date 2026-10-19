"""Drawing mazes and search results with Pillow."""

from typing import List, Optional

from PIL import Image, ImageDraw, ImageFont

from .maze import Maze
from .search import Result

WALL = (40, 44, 52)
FREE = (245, 245, 240)
EXPLORED = (190, 215, 240)
PATH = (230, 90, 60)
START = (60, 170, 90)
GOAL = (240, 190, 40)


def draw(maze: Maze, result: Optional[Result] = None, cell: int = 20) -> Image.Image:
    img = Image.new("RGB", (maze.width * cell, maze.height * cell), FREE)
    d = ImageDraw.Draw(img)

    explored = set(result.explored) if result else set()
    path = set(result.path or []) if result else set()

    for r in range(maze.height):
        for c in range(maze.width):
            pos = (r, c)
            if maze.is_wall(pos):
                color = WALL
            elif pos == maze.start:
                color = START
            elif pos == maze.goal:
                color = GOAL
            elif pos in path:
                color = PATH
            elif pos in explored:
                color = EXPLORED
            else:
                continue
            d.rectangle((c * cell, r * cell, (c + 1) * cell - 1, (r + 1) * cell - 1), fill=color)
    return img


def side_by_side(maze: Maze, results: List[Result], cell: int = 8) -> Image.Image:
    """One panel per algorithm with a caption underneath."""
    panels = [draw(maze, r, cell) for r in results]
    pw, ph = panels[0].size
    pad, caption = 16, 44
    out = Image.new("RGB", (len(panels) * (pw + pad) + pad, ph + 2 * pad + caption), (255, 255, 255))
    d = ImageDraw.Draw(out)
    try:
        font = ImageFont.load_default(size=18)
    except TypeError:  # older Pillow
        font = ImageFont.load_default()
    for i, (panel, res) in enumerate(zip(panels, results)):
        x = pad + i * (pw + pad)
        out.paste(panel, (x, pad))
        text = f"{res.algorithm.upper()}  path {res.length}  explored {len(res.explored)}"
        d.text((x, pad + ph + 12), text, fill=(30, 30, 30), font=font)
    return out
