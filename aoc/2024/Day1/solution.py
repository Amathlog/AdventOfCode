import copy
from typing import List, Tuple, Dict, Optional, Set
from aoc.common.parse_entry import parse_all
from aoc.common.utils import profile
from collections import defaultdict

entries, example_entries = parse_all(__file__, "entry.txt", "example.txt")

@profile
def part_one(entry: List[str]) -> int:
    first_list = []
    second_list = []
    for e in entry:
        first, second = e.split("   ")
        first_list.append(int(first))
        second_list.append(int(second))

    first_list.sort()
    second_list.sort()
    
    result = 0
    for first, second in zip(first_list, second_list):
        result += abs(first - second)

    return result


@profile
def part_two(entry: List[str]) -> int:
    first_list = []
    second_list = defaultdict(int)
    for e in entry:
        first, second = e.split("   ")
        first_list.append(int(first))
        second_list[int(second)] += 1
    
    result = 0
    for first in first_list:
        count = second_list[first]
        result += first * count

    return result


if __name__ == "__main__":
    print("Part 1 example:", part_one(example_entries))
    print("Part 1 entry:", part_one(entries))

    print("Part 2 example:", part_two(example_entries))
    print("Part 2 entry:", part_two(entries))
