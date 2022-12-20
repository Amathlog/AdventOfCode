from pathlib import Path
import os
import copy
from typing import List, Tuple, Dict

entry_file = Path(os.path.abspath(__file__)).parent / "entry.txt"
example_file = Path(os.path.abspath(__file__)).parent / "example.txt"

def parse_entry(path: str) -> List[int]:
    with path.open("r") as f:
        entries = f.readlines()

    for i in range(len(entries)):
        if entries[i][-1] == '\n':
            entries[i] = entries[i][:-1]

        entries[i] = int(entries[i])

    return entries

entries = parse_entry(entry_file)
example_entries = parse_entry(example_file)

class Node:
    def __init__(self, value: int, real_value: int):
        self.value = value
        self.real_value = real_value
        self.prev : "Node" = None
        self.next: "Node" = None


def print_all(start_node: Node):
    curr = start_node
    done = False
    while not done:
        print(f"{curr.real_value}, ", end="")
        curr = curr.next
        if curr == start_node:
            done = True
    print()


def solve(entries: List[int], encryption_key: int = 1, nb_mixing: int = 1) -> int:
    all_nodes = []
    zero_node = None
    for e in entries:
        real_value = e * encryption_key
        value = abs(real_value) % (len(entries) - 1)
        if real_value < 0:
            value = -value

        if abs(value) > (len(entries) - 1) // 2:
            temp = len(entries) - 1 - abs(value)
            value = temp if value < 0 else -temp

        all_nodes.append(Node(value, real_value))
        if e == 0:
            zero_node = all_nodes[-1]
        if len(all_nodes) > 1:
            all_nodes[-2].next = all_nodes[-1]
            all_nodes[-1].prev = all_nodes[-2]

    all_nodes[-1].next = all_nodes[0]
    all_nodes[0].prev = all_nodes[-1]

    verbose = False

    start_node = all_nodes[0]
    if verbose:
        print_all(start_node)

    for _ in range(nb_mixing):
        for node in all_nodes:
            offset = abs(node.value)
            if offset == 0:
                if verbose:
                    print(f"Moved {node.real_value} by {node.value}")
                    print_all(start_node)
                continue

            previous_node = node.prev
            next_node = node.next

            assert previous_node != next_node

            curr = node
            seen = set()
            for _ in range(offset):
                assert curr not in seen
                seen.add(curr)
                curr = curr.prev if node.value < 0 else curr.next

            # One more if we go backward
            if node.value < 0:
                curr = curr.prev

            previous_node.next = next_node
            next_node.prev = previous_node

            temp = curr.next
            curr.next = node
            node.prev = curr

            temp.prev = node
            node.next = temp

            assert temp != curr
            assert temp != node
            assert curr != node

            if node == start_node:
                start_node = next_node

            if verbose:
                print(f"Moved {node.real_value} by {node.value}")
                print_all(start_node)

    offsets = [1000, 2000, 3000]
    res = 0
    for offset in offsets:
        offset %= len(all_nodes)
        curr = zero_node
        for _ in range(offset):
            curr = curr.next
        res += curr.real_value

    return res
           

if __name__ == "__main__":
    print(f"Part 1: {solve(entries)}")
    print(f"Part 2: {solve(entries, 811589153, 10)}")