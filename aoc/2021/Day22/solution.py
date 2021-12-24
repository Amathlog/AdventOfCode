from pathlib import Path
import os
import copy
from typing import List, Optional, Tuple
import numpy as np

entry_file = Path(os.path.abspath(__file__)).parent / "entry.txt"
example_file = Path(os.path.abspath(__file__)).parent / "example.txt"
example2_file = Path(os.path.abspath(__file__)).parent / "example2.txt"

with entry_file.open("r") as f:
    entries = f.readlines()

for i in range(len(entries)):
    if entries[i][-1] == '\n':
        entries[i] = entries[i][:-1]

RangeTuple = Tuple[int, int]
ThreeRangeTuple = Tuple[RangeTuple, RangeTuple, RangeTuple]

# PART 1
def set_slice(entry: str, min_range: int, grid_: np.ndarray):
    value, rest = entry.split(" ")
    value = value == "on"
    ranges = []
    for coordinate in rest.split(","):
        coordinate = coordinate[2:]

        ranges.append([int(v) - min_range for v in coordinate.split("..")])
        if (ranges[-1][0] < min_range):
            ranges[-1][0] = min_range
        elif (ranges[-1][0] >= len(grid_)):
            return grid_

        if (ranges[-1][1] >= len(grid_)):
            ranges[-1][1] = len(grid_) - 1
        elif (ranges[-1][1] < min_range):
            return grid_

    grid_[ranges[0][0]:ranges[0][1] + 1, ranges[1][0]:ranges[1][1] + 1, ranges[2][0]:ranges[2][1] + 1] = value
    return grid_

def first_part():
    min_value = -50
    size = 101
    grid = np.zeros((size, size, size), dtype=np.bool)

    for e in entries:
        grid = set_slice(e, min_value, grid)

    print("First answer:", np.sum(grid))

# PART 2
class Cuboid:
    def __init__(self, x_min, x_max, y_min, y_max, z_min, z_max):
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max
        self.z_min = z_min
        self.z_max = z_max

    def intersection(self, other) -> bool:
        if self.x_max < other.x_min \
            or other.x_max < self.x_min \
            or self.y_max < other.y_min \
            or other.y_max < self.y_min \
            or self.z_max < other.z_min \
            or other.z_max < self.z_min:
            return False

        return True

    def is_in(self, other) -> bool:
        return self.x_min <= other.x_min and self.x_max >= other.x_max \
            and self.y_min <= other.y_min and self.y_max >= other.y_max \
            and self.z_min <= other.z_min and self.z_max >= other.z_max

    def compute_intersection(self, other) -> Optional[ThreeRangeTuple]:
        if not self.intersection(other):
            return None

        return (max(self.x_min, other.x_min), min(self.x_max, other.x_max)), \
               (max(self.y_min, other.y_min), min(self.y_max, other.y_max)), \
               (max(self.z_min, other.z_min), min(self.z_max, other.z_max))

    def compute_union(self, other) -> List["Cuboid"]:
        pass

    def can_merge(self, other) -> bool:
        if not self.intersection(other):
            return (other.x_min == self.x_max or other.x_max == self.x_min) and \
                (other.y_min == self.y_max or other.y_max == self.y_min) and \
                (other.z_min == self.z_max or other.z_max == self.z_min)

        else:
            pass
def intersect_cuboid():
    pass

if __name__ == "__main__":
    first_part()
