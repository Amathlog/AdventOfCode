import copy
from typing import List, Tuple, Dict, Optional, Set
from aoc.common.parse_entry import parse_all
from aoc.common.utils import profile

entries, example_entries = parse_all(__file__, "entry.txt", "example.txt")

@profile
def part_one(entry: List[str]) -> int:
    curr = 50
    res = 0
    for e in entry:
        clicks = int(e[1:])
        if e[0] == "L":
            clicks = -clicks
        
        curr += clicks
        while curr >= 100:
            curr -= 100
        while curr < 0:
            curr += 100

        if curr == 0:
            res += 1
    
    return res

@profile
def part_two(entry: List[str]) -> int:
    curr = 50
    res = 0
    for e in entry:
        clicks = int(e[1:])

        while abs(clicks) >= 100:
            res += 1
            clicks -= 100

        if clicks == 0:
            continue

        if e[0] == "L":
            clicks = -clicks

        was_zero = curr == 0
        
        curr += clicks

        if curr == 0:
            res += 1
        elif curr >= 100:
            res += 1
            curr -= 100
        elif curr < 0:
            curr += 100
            if not was_zero:
                res += 1
    
    return res


if __name__ == "__main__":
    print("Part 1 example:", part_one(example_entries))
    print("Part 1 entry:", part_one(entries))

    print("Part 2 example:", part_two(example_entries))
    print("Part 2 entry:", part_two(entries))
