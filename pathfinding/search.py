"""Search algorithms.

All four share the same loop; they only differ in which node the frontier
hands back next:

    DFS     stack                      - finds *a* path, often a long one
    BFS     queue                      - shortest path, explores a lot
    Greedy  priority = distance to B   - fast, but not always shortest
    A*      priority = cost + distance - shortest path, explores less than BFS

Distance is Manhattan distance, which never overestimates on a 4-connected
grid, so A* is guaranteed to return a shortest path.
"""

import heapq
import itertools
from collections import deque
from dataclasses import dataclass, field
from typing import Dict, List, Optional

from .maze import Cell, Maze


@dataclass
class Node:
    state: Cell
    action: Optional[tuple]
    parent: Optional["Node"]
    cost: int = 0


class StackFrontier:
    def __init__(self):
        self.items = []

    def add(self, node, priority=0):
        self.items.append(node)

    def remove(self):
        return self.items.pop()

    def empty(self):
        return not self.items


class QueueFrontier(StackFrontier):
    def __init__(self):
        self.items = deque()

    def remove(self):
        return self.items.popleft()


class PriorityFrontier:
    def __init__(self):
        self.heap = []
        self.counter = itertools.count()  # tie-breaker: first in, first out

    def add(self, node, priority=0):
        heapq.heappush(self.heap, (priority, next(self.counter), node))

    def remove(self):
        return heapq.heappop(self.heap)[2]

    def empty(self):
        return not self.heap


def manhattan(a: Cell, b: Cell) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


ALGORITHMS = {
    "dfs": (StackFrontier, lambda node, goal: 0),
    "bfs": (QueueFrontier, lambda node, goal: 0),
    "greedy": (PriorityFrontier, lambda node, goal: manhattan(node.state, goal)),
    "astar": (PriorityFrontier, lambda node, goal: node.cost + manhattan(node.state, goal)),
}


@dataclass
class Result:
    algorithm: str
    path: Optional[List[Cell]]          # cells from start to goal, None if unreachable
    actions: List[tuple] = field(default_factory=list)
    explored: List[Cell] = field(default_factory=list)  # in the order they were expanded

    @property
    def found(self):
        return self.path is not None

    @property
    def length(self):
        return len(self.path) - 1 if self.path else None


def solve(maze: Maze, algorithm: str = "astar") -> Result:
    frontier_cls, priority = ALGORITHMS[algorithm]
    frontier = frontier_cls()
    start = Node(maze.start, None, None, 0)
    frontier.add(start, priority(start, maze.goal))

    best_cost: Dict[Cell, int] = {maze.start: 0}
    explored: List[Cell] = []
    expanded = set()

    while not frontier.empty():
        node = frontier.remove()
        if node.state in expanded:
            continue
        expanded.add(node.state)
        explored.append(node.state)

        if node.state == maze.goal:
            path, actions = [], []
            while node is not None:
                path.append(node.state)
                if node.action:
                    actions.append(node.action)
                node = node.parent
            return Result(algorithm, path[::-1], actions[::-1], explored)

        for nxt, action in maze.neighbours(node.state):
            cost = node.cost + 1
            if nxt in expanded:
                continue
            # DFS keeps its original behaviour (no cost bookkeeping)
            if algorithm != "dfs" and cost >= best_cost.get(nxt, float("inf")):
                continue
            best_cost[nxt] = cost
            child = Node(nxt, action, node, cost)
            frontier.add(child, priority(child, maze.goal))

    return Result(algorithm, None, [], explored)
