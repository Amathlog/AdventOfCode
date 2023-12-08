from pathlib import Path
import os
import copy
from typing import List, Tuple, Dict
from aoc.common.parse_entry import parse_all
import numpy as np

entries, example_entries, example2_entries = parse_all(__file__, "entry.txt", "example.txt", "example2.txt")

class Node:
    def __init__(self, name: str, left: str, right: str):
        self.name = name
        self.left_name = left
        self.right_name = right

        self.left: "Node" = None
        self.right: "Node" = None

    def update(self, all_nodes: Dict[str, "Node"]):
        self.left = all_nodes[self.left_name]
        self.right = all_nodes[self.right_name]

    def __str__(self) -> str:
        return f"{self.name} = ({self.left.name}, {self.right.name})"
    
    def get_next(self, inst: str):
        return self.left if inst == "L" else self.right
    
class Map:
    def __init__(self, entry: List[str]) -> None:
        self.instructions = entry[0]
        self.nodes: Dict[str, List[Node]] = {}

        for e in entry[2:]:
            node_name = e[:3]
            left = e[7:10]
            right = e[12:15]

            self.nodes[node_name] = Node(node_name, left, right)

        for node in self.nodes.values():
            node.update(self.nodes)

    def __repr__(self) -> str:
        res = ""
        for node in self.nodes.values():
            res += str(node) + "\n"
        return res
    
    def progress(self, start: str, end: str):
        curr = self.nodes[start]
        i = 0
        steps = 0
        while curr.name != end:
            inst = self.instructions[i]
            i = (i + 1) % len(self.instructions)
            curr = curr.get_next(inst)
            steps += 1

        return steps
    
    # For each node, find all cycles with their corresponding instruction index
    # Then find the instruction index for all nodes would finish at this index
    # The result it the lcm of all those cyles.
    def progress_ghost(self, start_letter: str, end_letter: str):
        res = []
        for curr in [n for n in self.nodes.values() if n.name[-1] == start_letter]:
            i = 0
            inital_step = 0
            first_final_inst = 0
            step = 0
            stop = False
            all_inst = {}
            while not stop:
                if curr.name[-1] == end_letter:
                    if inital_step == 0:
                        inital_step = step
                        first_final_inst = i
                    else:
                        all_inst[i] = step - inital_step
                        stop = i == first_final_inst

                inst = self.instructions[i]
                i = (i + 1) % len(self.instructions)
                curr = curr.get_next(inst)
                step += 1

            res.append(all_inst[0])

        return np.lcm.reduce(res)


def part_one(entry: List[str]) -> int:
    return Map(entry).progress("AAA", "ZZZ")


def part_two(entry: List[str]) -> int:
    return Map(entry).progress_ghost("A", "Z")


if __name__ == "__main__":
    print("Part 1 example:", part_one(example_entries))
    print("Part 1 entry:", part_one(entries))

    print("Part 2 example:", part_two(example2_entries))
    print("Part 2 entry:", part_two(entries))

