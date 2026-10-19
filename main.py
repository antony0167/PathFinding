"""Maze solving with DFS, BFS, Greedy best-first search and A*.

Examples
    python main.py mazes/maze1.txt                     # A*, prints the path
    python main.py mazes/maze1.txt --algo dfs --show   # open the picture
    python main.py mazes/large.txt --compare --out images/comparison.png
    python main.py --generate 30x30 --save mazes/large.txt
"""

import argparse
import sys

from pathfinding.generate import generate
from pathfinding.maze import Maze
from pathfinding.render import draw, side_by_side
from pathfinding.search import ALGORITHMS, solve


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("maze", nargs="?", help="maze text file")
    ap.add_argument("--algo", default="astar", choices=sorted(ALGORITHMS))
    ap.add_argument("--compare", action="store_true", help="run every algorithm and compare")
    ap.add_argument("--out", help="save the picture to this file")
    ap.add_argument("--show", action="store_true", help="open the picture in an image viewer")
    ap.add_argument("--generate", metavar="ROWSxCOLS", help="generate a random maze instead of loading one")
    ap.add_argument("--save", help="where to write the generated maze")
    ap.add_argument("--seed", type=int)
    args = ap.parse_args(argv)

    if args.generate:
        rows, cols = (int(x) for x in args.generate.lower().split("x"))
        lines = generate(rows, cols, seed=args.seed)
        if args.save:
            with open(args.save, "w") as f:
                f.write("\n".join(lines) + "\n")
        maze = Maze(lines)
    elif args.maze:
        maze = Maze.from_file(args.maze)
    else:
        ap.error("give a maze file or --generate")

    if args.compare:
        results = [solve(maze, a) for a in ("dfs", "bfs", "greedy", "astar")]
        print(f"{'algorithm':<10}{'path length':>12}{'cells explored':>16}")
        for r in results:
            print(f"{r.algorithm:<10}{str(r.length):>12}{len(r.explored):>16}")
        img = side_by_side(maze, results)
    else:
        r = solve(maze, args.algo)
        if not r.found:
            print("no path found")
            return 1
        print(f"{r.algorithm}: path of {r.length} steps, explored {len(r.explored)} cells")
        print("actions:", r.actions)
        img = draw(maze, r)

    if args.out:
        img.save(args.out)
        print(f"saved {args.out}")
    if args.show:
        img.show()
    return 0


if __name__ == "__main__":
    sys.exit(main())
