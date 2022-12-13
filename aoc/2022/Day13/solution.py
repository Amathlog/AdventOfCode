from pathlib import Path
import os
import copy
from typing import List, Optional, Tuple

entry_file = Path(os.path.abspath(__file__)).parent / "entry.txt"
example_file = Path(os.path.abspath(__file__)).parent / "example.txt"

with entry_file.open("r") as f:
    entries = f.readlines()

for i in range(len(entries)):
    if entries[i][-1] == '\n':
        entries[i] = entries[i][:-1]


class Node:
    def __init__(self, value: Optional[int] = None):
        self.value: int = value
        self.children: List["Node"] = []

    @property
    def is_leaf(self):
        return self.value is not None

    def add_child(self, child: "Node"):
        self.children.append(child)

    @staticmethod
    def from_input(input: str) -> "Node":
        return Node.from_list_int(eval(input))

    @staticmethod
    def from_list_int(list_in: List) -> "Node":
        res = Node()
        for item in list_in:
            if type(item) is int:
                res.add_child(Node(item))
            else:
                res.add_child(Node.from_list_int(item))
        
        return res

    def __repr__(self) -> str:
        if self.value is not None:
            return str(self.value)
        
        return "[" + ",".join((str(c) for c in self.children)) + "]"

    def compare(self, other: "Node") -> int:
        if self.is_leaf and other.is_leaf:
            return self.value - other.value
        
        if self.is_leaf:
            temp_node = Node()
            temp_node.add_child(self)
            return temp_node.compare(other)
        
        if other.is_leaf:
            temp_node = Node()
            temp_node.add_child(other)
            return self.compare(temp_node)

        for node1, node2 in zip(self.children, other.children):
            res = node1.compare(node2)
            if res != 0:
                return res

        return len(self.children) - len(other.children)

    def __lt__(self, other: "Node") -> bool:
        return self.compare(other) < 0


if __name__ =="__main__":
    all_packets: List[Node] = []

    sum_of_valid_pairs = 0

    for i in range(len(entries) // 3 + 1):
        entry1 = entries[3*i]
        entry2 = entries[3*i + 1]

        node1 = Node.from_input(entry1)
        node2 = Node.from_input(entry2)

        all_packets.extend((node1, node2))

        # Right order
        if node1 < node2:
            sum_of_valid_pairs += i + 1

    print("Part 1: Sum of valid pairs =", sum_of_valid_pairs)

    # Adding 2 packets
    divider_packet1 = Node.from_list_int([[2]])
    divider_packet2 = Node.from_list_int([[6]])

    all_packets.extend((divider_packet1, divider_packet2))
    all_packets.sort()

    decoder_key = 0

    for i in range(len(all_packets)):
        if all_packets[i] == divider_packet1:
            decoder_key = i+1
        elif all_packets[i] == divider_packet2:
            decoder_key *= i+1
            break

    print("Part2: Decoder key =", decoder_key)