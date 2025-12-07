from collections import defaultdict
import copy
import itertools
from typing import List, Tuple, Dict, Optional, Set
from aoc.common.parse_entry import parse_all_multiple_parts, default_separator
from aoc.common.utils import profile

entries, example_entries = parse_all_multiple_parts(__file__, default_separator, 3, "entry.txt", "example.txt")

@profile
def part_one(entry: List[str]) -> int:
    mentors = 0

    res = 0
    for c in entry[0]:
        if c == "A":
            mentors += 1
        elif c == 'a':
            res += mentors

    return res

@profile
def part_two(entry: List[str]) -> int:
    mentors = defaultdict(int)
    res = defaultdict(int)
    for c in entry[0]:
        c_upper = c.upper()
        if c == c_upper:
            mentors[c] += 1
        else:
            res[c] += mentors[c_upper]

    return sum(res.values())

@profile
def part_three(entry: List[str]) -> int:
    mentors = defaultdict(int)
    squires = defaultdict(int)
    for i in range(1000):
        c = entry[0][i % len(entry[0])]
        c_upper = c.upper()
        if c == c_upper:
            mentors[c] += 1
        else:
            squires[c] += 1

    return sum(itertools.starmap(lambda a,b: a*b, zip(mentors.values(), squires.values()))) * (1000 / len(entry))


if __name__ == "__main__":
    print("Part 1 example:", part_one(example_entries[0]))
    print("Part 1 entry:", part_one(entries[0]))

    print("Part 2 example:", part_two(example_entries[1]))
    print("Part 2 entry:", part_two(entries[1]))

    print("Part 3 example:", part_three(example_entries[2]))
    print("Part 3 entry:", part_three(entries[2]))
