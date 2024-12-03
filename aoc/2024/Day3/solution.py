import copy
from typing import List, Tuple, Dict, Optional, Set
from aoc.common.parse_entry import parse_all
from aoc.common.utils import profile
import re

entries, example_entries = parse_all(__file__, "entry.txt", "example.txt")

@profile
def part_one(entry: List[str]) -> int:
    regex = "mul\((\d+),(\d+)\)"
    pattern = re.compile(regex)
    result = 0
    for e in entry:
        for a,b in pattern.findall(e):
            result += int(a) * int(b)
    return result


@profile
def part_two(entry: List[str]) -> int:
    regex = "(do\(\))|(mul\((\d+),(\d+)\))|(don't\(\))"
    pattern = re.compile(regex)
    result = 0
    enabled = True
    for e in entry:
        for find_result in pattern.findall(e):
            if len(find_result[0]) > 0 or len(find_result[-1]) > 0:
                enabled = len(find_result[0]) > 0
            elif enabled:
                result += int(find_result[2]) * int(find_result[3])
    return result


if __name__ == "__main__":
    print("Part 1 example:", part_one(example_entries))
    print("Part 1 entry:", part_one(entries))

    print("Part 2 example:", part_two(example_entries))
    print("Part 2 entry:", part_two(entries))
