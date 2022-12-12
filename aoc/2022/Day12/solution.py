from pathlib import Path
import os
import copy
from typing import List
import sys

entry_file = Path(os.path.abspath(__file__)).parent / "entry.txt"
example_file = Path(os.path.abspath(__file__)).parent / "example.txt"

with entry_file.open("r") as f:
    entries = f.readlines()

for i in range(len(entries)):
    if entries[i][-1] == '\n':
        entries[i] = entries[i][:-1]

class Node:
    def __init__(self, height: int):
        self.height = height
        self.neighbors = set()
        self.too_high_neighboors = set()

    def add_neighbor(self, other: "Node"):
        if other in self.neighbors or other in self.too_high_neighboors:
            return

        if other.height <= (self.height + 1):
            self.neighbors.add(other)
        else:
            self.too_high_neighboors.add(other)

        other.add_neighbor(self)


def print_nodes(nodes, start_node, end_node):
    for i in range(len(nodes)):
        for j in range(len(nodes[0])):
            node = nodes[i][j]
            if node == start_node:
                print("S", end="")
            elif node == end_node:
                print("E", end="")
            else:
                print(chr(ord('a') + node.height), end="")
        print()


def dijsktra(nodes: set[Node], start: Node, end: Node, reverse:bool = False) -> List[Node]:
    dist = {n: sys.maxsize for n in nodes}
    dist[start] = 0
    prev = {n: None for n in nodes}
    seen = set()
    all_nodes: List[Node] = sorted(list(nodes), key=lambda x: dist[x], reverse=True)

    while len(all_nodes) > 0:
        curr: Node = all_nodes.pop()
        if end is not None and curr == end:
            break

        if reverse and curr.height == 0:
            end = curr
            break

        seen.add(curr)

        update = False

        for neighbor in curr.neighbors:
            if neighbor in seen:
                continue

            if reverse:
                # In reverse, we can't go to a neighboor that is too high on the other way
                if curr in neighbor.too_high_neighboors:
                    continue

            new_dist = dist[curr] + 1
            if new_dist < dist[neighbor]:
                dist[neighbor] = new_dist
                prev[neighbor] = curr
                update = True

        if reverse:
            for neighbor in curr.too_high_neighboors:
                if neighbor in seen:
                    continue

                new_dist = dist[curr] + 1
                if new_dist < dist[neighbor]:
                    dist[neighbor] = new_dist
                    prev[neighbor] = curr
                    update = True

        if update:
            all_nodes.sort(key=lambda x: dist[x], reverse=True)


    if prev[end] != None:
        res = [end]
        curr = end
        while curr != start:
            res.append(prev[curr])
            curr = prev[curr]
        return res

    return []

def parse_nodes():
    start_node = None
    end_node = None
    nodes = [[None for _ in range(len(e))] for e in entries]
    nodes_set = set()

    for i, e in enumerate(entries):
        for j, c in enumerate(e):
            if c == "S":
                start_node = Node(0)
                nodes[i][j] = start_node
            elif c == "E":
                end_node = Node(25)
                nodes[i][j] = end_node
            else:
                nodes[i][j] = Node(ord(c) - ord('a'))

            if i != 0:
                nodes[i][j].add_neighbor(nodes[i-1][j])
            if j != 0:
                nodes[i][j].add_neighbor(nodes[i][j-1])

            nodes_set.add(nodes[i][j])

    return start_node, end_node, nodes, nodes_set

if __name__ == "__main__":
    start_node, end_node, nodes, nodes_set = parse_nodes()

    part1 = dijsktra(nodes_set, start_node, end_node)
    print(f"Part1: shortest = {len(part1) - 1}")

    part2 = dijsktra(nodes_set, end_node, None, True)
    print(f"Part2: shortest = {len(part2) - 1}")