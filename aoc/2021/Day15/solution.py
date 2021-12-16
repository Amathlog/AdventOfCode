from pathlib import Path
import os
from typing import Callable, Dict, List
from aoc.utils import neighboor_iter
import heapq

entry_file = Path(os.path.abspath(__file__)).parent / "entry.txt"
example_file = Path(os.path.abspath(__file__)).parent / "example.txt"

with entry_file.open("r") as f:
    entries = f.readlines()

for i in range(len(entries)):
    if entries[i][-1] == '\n':
        entries[i] = entries[i][:-1]


class Node:
    def __init__(self, x: int, y: int, value: int) -> None:
        self.value = value
        self.x = x
        self.y = y
        self.connections = set()

    def add_connection(self, c):
        self.connections.add(c)

    def __lt__(self, other):
        return self.value < other.value


class Graph:
    def __init__(self, grid, repeat:int = 1) -> None:
        self.nodes = {}
        self.size_x = len(grid) * repeat
        self.size_y = len(grid[0]) * repeat

        self.small_size_x = len(grid)
        self.small_size_y = len(grid[0])

        for x in range(self.size_x):
            for y in range(self.size_y):
                value = (int(grid[x % self.small_size_x][y % self.small_size_y]) + x // self.small_size_x + y // self.small_size_y)
                if value >= 10:
                    value = value % 10 + 1
                new_node = Node(x, y, value)
                self.nodes[(x, y)] = new_node
                for coor in neighboor_iter(x, y, self.size_x, self.size_y, discard_diagonal=True):
                    if coor in self.nodes:
                        new_node.add_connection(self.nodes[coor])
                        self.nodes[coor].add_connection(new_node)

    @property
    def start_node(self):
        return self.nodes[(0, 0)]

    @property
    def end_node(self):
        return self.nodes[(self.size_x - 1, self.size_y - 1)]


def a_star(start_node: Node, end_node: Node, heuristic: Callable[[Node], int]):
    open_set = []
    came_from = {}
    g_score = {start_node: 0}
    f_score = {start_node: heuristic(start_node)}
    heapq.heappush(open_set, (f_score[start_node], start_node))
    
    while len(open_set) > 0:
        _, curr = heapq.heappop(open_set)
        if curr == end_node:
            break

        for c in curr.connections:
            tentative_gScore = g_score[curr] + c.value
            if c not in g_score or tentative_gScore < g_score[c]:
                came_from[c] = curr
                g_score[c] = tentative_gScore
                f_score[c] = tentative_gScore + heuristic(c)
                if c not in open_set:
                    heapq.heappush(open_set, (f_score[c], c))

    return came_from

def count_risk(start: Node, end: Node, l: Dict[Node, Node]) -> int:
    curr = end
    cost = 0
    while curr is not None:
        cost += curr.value
        curr = l[curr]
        if curr == start:
            break

    return cost


if __name__ == "__main__":
    import time
    graph = Graph(entries)
    start = time.perf_counter()
    prev = a_star(graph.start_node, graph.end_node, lambda x: abs(graph.end_node.x - x.x) + abs(graph.end_node.y - x.y))
    print("First answer time:", time.perf_counter() - start)
    print("First answer:", count_risk(graph.start_node, graph.end_node, prev))

    graph = Graph(entries, 5)
    start = time.perf_counter()
    prev = a_star(graph.start_node, graph.end_node, lambda x: abs(graph.end_node.x - x.x) + abs(graph.end_node.y - x.y))
    print("Second answer time:", time.perf_counter() - start)
    print("Second answer:", count_risk(graph.start_node, graph.end_node, prev))