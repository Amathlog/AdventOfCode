import copy
from typing import List, Tuple, Dict, Optional, Set
from aoc.common.parse_entry import parse_all
from aoc.common.utils import profile

entries, example_entries = parse_all(__file__, "entry.txt", "example.txt")


class Node:
    def __init__(self, c: str):
        self.c = c
        self.leaf = False
        self.children: Dict[str, Node] = {}
    
    def add_children(self, pattern: str):
        if len(pattern) == 0:
            self.leaf = True
            return
        
        new_c = pattern[0]
        if new_c not in self.children:
            self.children[new_c] = Node(new_c)

        self.children[new_c].add_children(pattern[1:])

    def valid_indexes(self, design: str) -> List[int]:
        res = []
        if self.leaf:
            res = [0]

        if len(design) == 0 or design[0] not in self.children:
            return res
        
        return res + [x + 1 for x in self.children[design[0]].valid_indexes(design[1:])]


def match(patterns: "Node", design: str, seen_match: Dict[str, int]) -> int:
    if len(design) == 0:
       return 1

    if design in seen_match:
        return seen_match[design]

    nb_matches = 0
    for idx in patterns.valid_indexes(design):
        nb_matches += match(patterns, design[idx:], seen_match)
    
    seen_match[design] = nb_matches

    return nb_matches


@profile
def solve(entry: List[str]) -> int:
    patterns = Node(None)
    for pattern in entry[0].split(", "):
        patterns.add_children(pattern)
    
    count_part1 = 0
    count_part2 = 0
    seen_match = {}
    for design in entry[2:]:
        res = match(patterns, design, seen_match)
        count_part2 += res
        if res > 0:
            count_part1 += 1

    print(f"Memoisation size: {len(seen_match)}")

    return count_part1, count_part2


if __name__ == "__main__":
    print("Part 1 and 2 example:", solve(example_entries))
    print("Part 1 and 2 entry:", solve(entries))
