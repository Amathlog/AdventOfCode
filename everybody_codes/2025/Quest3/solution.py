import copy
from typing import List, Tuple, Dict, Optional, Set
from aoc.common.parse_entry import parse_all_multiple_parts, default_separator
from aoc.common.utils import profile

entries, example_entries = parse_all_multiple_parts(__file__, default_separator, 3, "entry.txt", "example.txt")

@profile
def part_one(entry: List[str]) -> int:
    entry = sorted([int(x) for x in entry[0].split(",")], reverse=True)
    seen = set()
    res = 0
    for e in entry:
        if e not in seen:
            res += e
            seen.add(e)

    return res
    

@profile
def part_two(entry: List[str]) -> int:
    entry = sorted([int(x) for x in entry[0].split(",")])
    seen = set()
    res = 0
    for e in entry:
        if len(seen) >= 20:
            break
        if e not in seen:
            res += e
            seen.add(e)

    return res

@profile
def part_three(entry: List[str]) -> int:
    entry = sorted([int(x) for x in entry[0].split(",")], reverse=True)
    res = 0
    while len(entry) > 0:
        seen = set()
        remaining = []
        for e in entry:
            if e not in seen:
                seen.add(e)
            else:
                remaining.append(e)
        
        res += 1
        entry = remaining
        
    return res


if __name__ == "__main__":
    print("Part 1 example:", part_one(example_entries[0]))
    print("Part 1 entry:", part_one(entries[0]))

    print("Part 2 example:", part_two(example_entries[1]))
    print("Part 2 entry:", part_two(entries[1]))

    print("Part 3 example:", part_three(example_entries[2]))
    print("Part 3 entry:", part_three(entries[2]))
