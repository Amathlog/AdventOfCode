import copy
from typing import List, Tuple, Dict, Optional, Set
from aoc.common.parse_entry import parse_all
from aoc.common.utils import profile
from aoc.common.range import Range

entries, example_entries = parse_all(__file__, "entry.txt", "example.txt")

@profile
def part_one(entry: List[str]) -> int:
    for i in range(len(entry)):
        if entry[i] == "":
            cut = i
            break

    ranges = Range.reduce([Range(*map(int, e.split("-"))) for e in entry[:cut]], inclusive=True)
    
    count = 0
    for id in entry[cut+1:]:
        id = int(id)
        for r in ranges:
            if r.min > id:
                break

            if r.contains(id, inclusive=True):
                count += 1
    return count

@profile
def part_two(entry: List[str]) -> int:
    for i in range(len(entry)):
        if entry[i] == "":
            cut = i
            break

    count = 0
    ranges = Range.reduce([Range(*map(int, e.split("-"))) for e in entry[:cut]], inclusive=True)
    for r in ranges:
        count += (r.max - r.min + 1)

    return count

if __name__ == "__main__":
    print("Part 1 example:", part_one(example_entries))
    print("Part 1 entry:", part_one(entries))

    print("Part 2 example:", part_two(example_entries))
    print("Part 2 entry:", part_two(entries))
