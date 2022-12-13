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

def extract_list(input: str) -> str:
    if input == "" or input[0] != "[":
        return ""

    i = 1
    sub_lists = 0
    while i < len(input):
        if input[i] == "[":
            sub_lists += 1
        elif input[i] == "]":
            sub_lists -= 1
            if sub_lists == -1:
                return input[:i+1]
        
        i += 1

    return ""


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
        if input == "":
            return Node()

        if input[0] != "[":
            return Node(int(input))

        res = Node()
        i = 1
        while i < len(input) - 1:
            if input[i] == "[":
                sub_list = extract_list(input[i:])
                assert sub_list != ""

                res.add_child(Node.from_input(sub_list))
                i += len(sub_list)
            elif input[i] == ",":
                i += 1
            else:
                value = input[i:].split(",")[0]
                int_value = int(value) if value[-1] != "]" else int(value[:-1])
                res.add_child(Node(int_value))
                i += len(value)

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
    pairs: List[Tuple[Node, Node]] = []
    all_packets: List[Node] = []

    part1_res = 0

    for i in range(len(entries) // 3 + 1):
        entry1 = entries[3*i]
        entry2 = entries[3*i + 1]

        pairs.append((Node.from_input(entry1), Node.from_input(entry2)))
        all_packets.extend(pairs[-1])

        comparison = pairs[-1][0].compare(pairs[-1][1])
        if comparison < 0:
            # Right order
            part1_res += i + 1

    print("Part 1: Sum of valid pairs =", part1_res)

    # Adding 2 packets
    divider_packet1 = Node()
    temp = Node()
    temp.add_child(Node(2))
    divider_packet1.add_child(temp)
    all_packets.append(divider_packet1)

    divider_packet2 = Node()
    temp2 = Node()
    temp2.add_child(Node(6))
    divider_packet2.add_child(temp2)
    all_packets.append(divider_packet2)

    all_packets.sort()

    part2_res = 1

    for i in range(len(all_packets)):
        if all_packets[i] == divider_packet1:
            part2_res *= i+1
        
        elif all_packets[i] == divider_packet2:
            part2_res *= i+1
            break

    print("Part2: Decoder key =", part2_res)