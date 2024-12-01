import copy
from typing import List, Tuple, Dict, Optional, Set
from aoc.common.parse_entry import parse_all_multiple_parts, default_separator
from aoc.common.utils import profile

entries, example_entries = parse_all_multiple_parts(__file__, default_separator, 3, "entry.txt", "example.txt")

@profile
def part_one_and_two(entry: List[str]) -> int:
    min_height = 99999999999999
    heights = []
    for e in entry:
        heights.append(int(e))
        if heights[-1] < min_height:
            min_height = heights[-1]

    return sum([h - min_height for h in heights])

@profile
def part_three(entry: List[str]) -> int:
    heights = []
    for e in entry:
        heights.append(int(e))

    heights.sort()
    median = heights[len(heights) // 2]
    return sum([abs(h - median) for h in heights])


if __name__ == "__main__":
    print("Part 1 example:", part_one_and_two(example_entries[0]))
    print("Part 1 entry:", part_one_and_two(entries[0]))

    print("Part 2 example:", part_one_and_two(example_entries[1]))
    print("Part 2 entry:", part_one_and_two(entries[1]))

    print("Part 3 example:", part_three(example_entries[2]))
    print("Part 3 entry:", part_three(entries[2]))
