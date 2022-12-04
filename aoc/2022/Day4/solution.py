from pathlib import Path
import os
import copy
from typing import Tuple

class Range:
    def __init__(self, min: int, max: int):
        self.min = min
        self.max = max

    @staticmethod
    def from_input(input: str) -> "Range":
        in_min, in_max = input.split("-")
        return Range(int(in_min), int(in_max))

    def is_valid(self) -> bool:
        return self.min <= self.max

    def get_intersection(self, other: "Range") -> Tuple[bool, "Range"]:
        res = Range(max([self.min, other.min]), min([self.max, other.max]))
        return res.is_valid(), res

    def __repr__(self) -> str:
        return f"{self.min}-{self.max}"

    def __eq__(self, other: "Range") -> bool:
        return self.min == other.min and self.max == other.max

entry_file = Path(os.path.abspath(__file__)).parent / "entry.txt"
example_file = Path(os.path.abspath(__file__)).parent / "example.txt"

with entry_file.open("r") as f:
    entries = f.readlines()

for i in range(len(entries)):
    if entries[i][-1] == '\n':
        entries[i] = entries[i][:-1]


ranges = [tuple((Range.from_input(i) for i in e.split(','))) for e in entries]

count_part1 = 0
count_part2 = 0
for a, b in ranges:
    valid, intersect = a.get_intersection(b)
    if (valid):
        count_part2 += 1
        if (intersect == a or intersect == b):
            count_part1 += 1

print(f"Part 1: Number of fully overlap ranges = {count_part1}")
print(f"Part 2: Number of overlap ranges = {count_part2}")