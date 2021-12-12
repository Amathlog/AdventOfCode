from pathlib import Path
import os
from typing import List, Optional, Set, Dict
from collections import defaultdict

entry_file = Path(os.path.abspath(__file__)).parent / "entry.txt"
example_file = entry_file.parent / "example.txt"

with entry_file.open("r") as f:
    entries = f.readlines()

for i in range(len(entries)):
    if entries[i][-1] == '\n':
        entries[i] = entries[i][:-1]


def is_upper(name: str) -> bool:
    return ord(name[0]) >= ord('A') and ord(name[0]) <= ord('Z')


class Node:
    def __init__(self, name: str):
        self.name = name
        self.connections: Set[Node] = set()
        self.is_big = is_upper(self.name)

    def add_connection(self, node: None):
        self.connections.add(node)

    def __repr__(self) -> str:
        return f"{self.name} (Big: {'True' if self.is_big else 'False'}): " + ", ".join([c.name for c in self.connections])


class Graph:
    def __init__(self, connections: List[str]):
        self.nodes: Dict[str, Node] = {}

        for c in connections:
            in_, out_ = c.split("-")
            if in_ in self.nodes:
                in_node = self.nodes[in_]
            else:
                in_node = Node(in_)
                self.nodes[in_] = in_node

            if out_ in self.nodes:
                out_node = self.nodes[out_]
            else:
                out_node = Node(out_)
                self.nodes[out_] = out_node

            in_node.add_connection(out_node)
            out_node.add_connection(in_node)

    @property
    def start_node(self) -> Optional[Node]:
        try:
            return self.nodes["start"]
        except KeyError:
            return None

    @property
    def end_node(self) -> Optional[Node]:
        try:
            return self.nodes["end"]
        except KeyError:
            return None

    def __repr__(self) -> str:
        res = ""
        for n in self.nodes.values():
            res += str(n) + "\n"

        return res

def find_all_paths_to_end(start_node: Node, graph: Graph, max_small:int, seen_caves: Optional[Dict[Node, int]] = None, multiple_seen_node: Optional[Node] = None) -> List[List[Node]]:
    end_node = graph.end_node
    if seen_caves is None:
        seen_caves = defaultdict(int)

    res = []

    if start_node == end_node:
        return [[end_node]]

    for node in start_node.connections:
        max_value = max_small if multiple_seen_node is None or node == multiple_seen_node else 1
        if seen_caves[node] == max_value:
            continue

        if node == graph.start_node:
            continue

        if not node.is_big:
            # Check if there is already a value at more than 1, if so, we cannot visit this cave
            if multiple_seen_node is not None and node != multiple_seen_node and seen_caves[node] == 1:
                continue
            seen_caves[node] += 1
            if seen_caves[node] > 1:
                multiple_seen_node = node

        all_paths = find_all_paths_to_end(node, graph, max_small, seen_caves, multiple_seen_node)
        for i in range(len(all_paths)):
            all_paths[i].insert(0, start_node)

        if not node.is_big:
            seen_caves[node] -= 1
            if multiple_seen_node is not None and node == multiple_seen_node and seen_caves[node] <= 1:
                multiple_seen_node = None

        res.extend(all_paths)

    return res


if __name__ == "__main__":
    graph = Graph(entries)
    res = find_all_paths_to_end(graph.start_node, graph, 1)

    print("First answer:", len(res))

    res = find_all_paths_to_end(graph.start_node, graph, 2)

    print("Second answer:", len(res))
