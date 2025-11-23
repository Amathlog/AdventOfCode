import copy
from typing import List, Tuple, Dict, Optional, Set
from aoc.common.parse_entry import parse_all_multiple_parts, default_separator
from aoc.common.utils import profile
import math

entries, example_entries = parse_all_multiple_parts(__file__, default_separator, 3, "entry.txt", "example.txt")

@profile
def part_one(entry: List[str]) -> int:
    gears = [int(x) for x in entry]

    final_ratio = 1
    for i in range(len(gears) - 1):
        final_ratio *= gears[i]/gears[i+1]
        
    return math.floor(2025 * final_ratio)

@profile
def part_two(entry: List[str]) -> int:
    gears = [int(x) for x in entry]

    final_ratio = 1
    for i in range(len(gears) - 1):
        final_ratio *= gears[i]/gears[i+1]

    return math.ceil(10000000000000 / final_ratio)

@profile
def part_three(entry: List[str]) -> int:
    gears = [(0, int(entry[0]))]
    for e in entry[1:-1]:
        a,b = e.split("|")
        gears.append((int(a), int(b)))
    gears.append((int(entry[-1]), 0))

    final_ratio = 1
    for i in range(len(gears) - 1):
        final_ratio *= gears[i][1]/gears[i+1][0]
        
    return math.floor(100 * final_ratio)


if __name__ == "__main__":
    print("Part 1 example:", part_one(example_entries[0]))
    print("Part 1 entry:", part_one(entries[0]))

    print("Part 2 example:", part_two(example_entries[1]))
    print("Part 2 entry:", part_two(entries[1]))

    print("Part 3 example:", part_three(example_entries[2]))
    print("Part 3 entry:", part_three(entries[2]))
