import copy
from typing import List, Tuple, Dict, Optional, Set
from aoc.common.parse_entry import parse_all_multiple_parts, default_separator
from aoc.common.utils import profile

entries, example_entries = parse_all_multiple_parts(__file__, default_separator, 3, "entry.txt", "example.txt")

@profile
def part_one(entry: List[str]) -> int:
    names = entry[0].split(',')
    instructions = entry[2].split(',')
    last = len(names) - 1
    curr = 0
    for inst in instructions:
        move = int(inst[1:])
        if inst[0] == "L":
            move = -move

        curr += move
        curr = max(0, min(last, curr))
        
    return names[curr]


@profile
def part_two(entry: List[str]) -> int:
    names = entry[0].split(',')
    instructions = entry[2].split(',')
    size = len(names)
    curr = 0
    for inst in instructions:
        move = int(inst[1:])
        if inst[0] == "L":
            move = -move

        curr += move
        while (curr < 0):
            curr += size
        while (curr >= size):
            curr -= size

    return names[curr]

@profile
def part_three(entry: List[str]) -> int:
    names = entry[0].split(',')
    instructions = entry[2].split(',')
    size = len(names)
    indices = list(range(size))

    for inst in instructions:
        cursor = int(inst[1:])
        while (cursor >= size):
            cursor -= size
        if inst[0] == "L":
            cursor = -cursor

        indices[0], indices[cursor] = indices[cursor], indices[0]

    return names[indices[0]]


if __name__ == "__main__":
    print("Part 1 example:", part_one(example_entries[0]))
    print("Part 1 entry:", part_one(entries[0]))

    print("Part 2 example:", part_two(example_entries[1]))
    print("Part 2 entry:", part_two(entries[1]))

    print("Part 3 example:", part_three(example_entries[2]))
    print("Part 3 entry:", part_three(entries[2]))
