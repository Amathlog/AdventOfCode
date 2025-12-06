import copy
from typing import List, Tuple, Dict, Optional, Set
from aoc.common.parse_entry import parse_all
from aoc.common.utils import profile

entries, example_entries = parse_all(__file__, "entry.txt", "example.txt")

def find_highest_in_range(e: List[str], start: int, end: int):
    highest = None
    range = e[start:end]
    for i, c in enumerate(range):
        if highest is None or c > highest[0]:
            highest = (c, start+i)

    return highest

@profile
def part_one(entry: List[str]) -> int:
    res = 0
    for e in entry:
        first_highest = find_highest_in_range(e, 0, -1)
        second_highest = find_highest_in_range(e, first_highest[1]+1, len(e))
        res += int(first_highest[0] + second_highest[0])
       
    return res


@profile
def part_two(entry: List[str]) -> int:
    res = 0
    for e in entry:
        heighest = []
        start = 0
        for i in range(12):
            end = len(e) - 11 + i
            c, idx = find_highest_in_range(e, start, end)

            heighest.append(c)
            start = idx+1

        res += int(''.join(heighest))
       
    return res


if __name__ == "__main__":
    print("Part 1 example:", part_one(example_entries))
    print("Part 1 entry:", part_one(entries))

    print("Part 2 example:", part_two(example_entries))
    print("Part 2 entry:", part_two(entries))
