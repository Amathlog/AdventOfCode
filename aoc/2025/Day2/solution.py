import copy
from typing import List, Tuple, Dict, Optional, Set
from aoc.common.parse_entry import parse_all
from aoc.common.utils import profile
import math

entries, example_entries = parse_all(__file__, "entry.txt", "example.txt")

def is_valid_part1(id: int):
    id_str = str(id)
    if len(id_str) % 2 == 1:
        return True
    
    return id_str[:len(id_str)//2] != id_str[len(id_str)//2:]

def is_valid_part2(id: int):
    id_str = str(id)
    max_idx = len(id_str) // 2

    for length in range(1, max_idx+1):
        if len(id_str) % length != 0:
            continue
        token = id_str[:length]
        curr = length
        repeat = True
        while curr + length <= len(id_str):
            if id_str[curr:curr+length] != token:
                repeat = False
                break

            curr += length

        if repeat:
            return False
        
    return True

class Range:
    def __init__(self, min: int, max: int):
        self.min = min
        self.max = max

    @staticmethod
    def construct(entry: str) -> "Range":
        return Range(*(int(x) for x in entry.split("-")))
    
    @staticmethod
    def construct_list(entries: str) -> List["Range"]:
        return [Range.construct(e) for e in entries.split(",")]
    
    def get_sum_invalid_id_part1(self) -> int:
        res = 0
        for i in range(self.min, self.max + 1):
            if not is_valid_part1(i):
                res += i
        return res
    
    def get_sum_invalid_id_part2(self) -> int:
        res = 0
        for i in range(self.min, self.max + 1):
            if not is_valid_part2(i):
                res += i
        return res

@profile
def part_one(entry: List[str]) -> int:
    ranges = Range.construct_list(entry[0])
    return sum(map(Range.get_sum_invalid_id_part1, ranges))

@profile
def part_two(entry: List[str]) -> int:
    ranges = Range.construct_list(entry[0])
    return sum(map(Range.get_sum_invalid_id_part2, ranges))


if __name__ == "__main__":
    print("Part 1 example:", part_one(example_entries))
    print("Part 1 entry:", part_one(entries))

    print("Part 2 example:", part_two(example_entries))
    print("Part 2 entry:", part_two(entries))
