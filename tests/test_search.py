from collections import deque

import pytest

from pathfinding.generate import generate
from pathfinding.maze import Maze
from pathfinding.search import solve

SMALL = ["###B#",
         "### #",
         "##  #",
         "## ##",
         "A  ##"]


def shortest_length(maze):
    """Reference answer with a plain BFS over distances."""
    dist = {maze.start: 0}
    q = deque([maze.start])
    while q:
        cur = q.popleft()
        for nxt, _ in maze.neighbours(cur):
            if nxt not in dist:
                dist[nxt] = dist[cur] + 1
                q.append(nxt)
    return dist.get(maze.goal)


def valid_path(maze, path):
    assert path[0] == maze.start and path[-1] == maze.goal
    for a, b in zip(path, path[1:]):
        assert abs(a[0] - b[0]) + abs(a[1] - b[1]) == 1
        assert not maze.is_wall(b)


@pytest.mark.parametrize("algo", ["dfs", "bfs", "greedy", "astar"])
def test_small_maze(algo):
    m = Maze(SMALL)
    r = solve(m, algo)
    assert r.found
    valid_path(m, r.path)


@pytest.mark.parametrize("seed", range(10))
def test_bfs_and_astar_are_optimal(seed):
    m = Maze(generate(15, 15, loops=0.15, seed=seed))
    best = shortest_length(m)
    assert solve(m, "bfs").length == best
    assert solve(m, "astar").length == best
    for algo in ("dfs", "greedy"):
        r = solve(m, algo)
        valid_path(m, r.path)
        assert r.length >= best


def test_astar_explores_no_more_than_bfs():
    m = Maze(generate(25, 25, loops=0.1, seed=7))
    assert len(solve(m, "astar").explored) <= len(solve(m, "bfs").explored)


def test_unreachable_goal():
    m = Maze(["A#B"])
    assert not solve(m, "astar").found


def test_ragged_rows_are_padded_with_walls():
    m = Maze(["A ", "  B"])
    assert m.width == 3 and m.is_wall((0, 2))
