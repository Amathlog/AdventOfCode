from __future__ import annotations
from pathlib import Path
import os
from typing import Dict, Set
from copy import deepcopy

entry_file = Path(os.path.abspath(__file__)).parent / "entry.txt"

class Node:
    def __init__(self, name: str):
        self.name = name
        self.children: Dict[Node, int] = {}
        self.parents:Set = set()

    def add_parent(self, parent: Node):
        self.parents.add(parent)

    def add_child(self, child: Node, number: int):
        self.children[child] = number
        child.add_parent(self)


all_data: Dict[str, Node] = {}


with entry_file.open("r") as f:
    entries = f.readlines()

for entry in entries:
    entry = entry.split(" ")
    # Pattern:
    # light red bags contain 1 bright white bag, 2 muted yellow bags.
    # bright white bags contain 1 shiny gold bag.
    # faded blue bags contain no other bags.

    name = " ".join(entry[:2])
    all_data[name] = Node(name)

for entry in entries:
    entry = entry.split(" ")

    if entry[4] == "no":
        continue

    name = " ".join(entry[:2])

    i = 4
    while i < len(entry):
        number = int(entry[i])
        color = " ".join(entry[i+1:i+3])
        all_data[name].add_child(all_data[color], number)
        i += 4

target = "shiny gold"
stack = list(all_data[target].parents)

res = set()

while len(stack) != 0:
    node = stack.pop()
    if node in res:
        continue
    res.add(node)

    if len(node.parents) != 0:
        stack.extend(list(node.parents))

print("First response:", len(res))

def find_all_children(node: Node) -> int:
    if len(node.children) == 0:
        return 1
    
    res = 1
    for child, number in node.children.items():
        res += number * find_all_children(child)
    
    return res

print("Second response:", find_all_children(all_data[target]) - 1)
