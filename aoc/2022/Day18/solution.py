from pathlib import Path
import os
import copy
from typing import List, Tuple, Dict
import sys

entry_file = Path(os.path.abspath(__file__)).parent / "entry.txt"
example_file = Path(os.path.abspath(__file__)).parent / "example.txt"

class LavaDroplet:
    def __init__(self, coord: Tuple[int, int, int]):
        self.x, self.y, self.z = coord
        self.touching = 0

    def __repr__(self) -> str:
        return str((self.x, self.y, self.z))

    def update_touching(self, others: List["LavaDroplet"]):
        for other in others:
            diff = (abs(self.x - other.x), abs(self.y - other.y), abs(self.z - other.z))
            if diff[0] > 1 or diff[1] > 1 or diff[2] > 1:
                continue

            if diff in [(1, 0, 0), (0, 1, 0), (0, 0, 1)]:
                    self.touching += 1
                    other.touching += 1

    def update_unreachable(self, unreachable_air: set[Tuple[int, int, int]]):
        candidates = [
            (self.x + 1, self.y, self.z),
            (self.x - 1, self.y, self.z),
            (self.x, self.y + 1, self.z),
            (self.x, self.y - 1, self.z),
            (self.x, self.y, self.z + 1),
            (self.x, self.y, self.z - 1)
            ]

        for c in candidates:
            if c in unreachable_air:
                self.touching += 1

    def get_non_covered_surface(self):
        assert self.touching <= 6
        return 6 - self.touching

def flow3d(entries: List[LavaDroplet]):
    # Find the boundaries
    x_min, y_min, z_min = (sys.maxsize,) * 3
    x_max, y_max, z_max = (-999999,) * 3

    all_lava_droplets = set()

    for e in entries:
        x_min = min(x_min, e.x)
        y_min = min(y_min, e.y)
        z_min = min(z_min, e.z)
        x_max = max(x_max, e.x)
        y_max = max(y_max, e.y)
        z_max = max(z_max, e.z)
        all_lava_droplets.add((e.x, e.y, e.z))

    # Add padding
    x_min -= 1
    y_min -= 1
    z_min -= 1
    x_max += 1
    y_max += 1
    z_max += 1

    all_air_droplets = set(((i,j,k) for i in range(x_min, x_max+1) for j in range(y_min, y_max+1) for k in range(z_min, z_max+1))).difference(all_lava_droplets)
    all_air_droplets_reachable = set()

    stack = [(x_min, y_min, z_min)]

    while len(stack) != 0:
        current = stack.pop()
        if current in all_air_droplets_reachable:
            continue

        all_air_droplets_reachable.add(current)
        
        candidates = [
            (current[0] + 1, current[1], current[2]),
            (current[0] - 1, current[1], current[2]),
            (current[0], current[1] + 1, current[2]),
            (current[0], current[1] - 1, current[2]),
            (current[0], current[1], current[2] + 1),
            (current[0], current[1], current[2] - 1)
            ]

        for c in candidates:
            if c[0] < x_min or c[0] > x_max or c[1] < y_min or c[1] > y_max or c[2] < z_min or c[2] > z_max:
                continue

            if c in all_lava_droplets:
                continue

            stack.append(c)

    unreachable_air_droplets = all_air_droplets.difference(all_air_droplets_reachable)

    for e in entries:
        e.update_unreachable(unreachable_air_droplets)


def parse_entry(path: str) -> List[LavaDroplet]:
    with path.open("r") as f:
        entries = f.readlines()

    for i in range(len(entries)):
        if entries[i][-1] == '\n':
            entries[i] = entries[i][:-1]

        entries[i] = LavaDroplet(tuple(int(e) for e in entries[i].split(",")))

    return entries

entries = parse_entry(entry_file)
example_entries = parse_entry(example_file)
simple_entries = [LavaDroplet((1, 1, 1)), LavaDroplet((2, 1, 1))]
another_simple_entries = [LavaDroplet((1, 1, 1)), LavaDroplet((2, 1, 1)), LavaDroplet((4, 1, 1)), LavaDroplet((3, 1, 1))]

def solve(entries: List[LavaDroplet]):
    for i, entry in enumerate(entries):
        if i == len(entries) - 1:
            continue
        entry.update_touching(entries[i+1:])

    print("Part 1: Result =", sum((e.get_non_covered_surface() for e in entries)))

    flow3d(entries)

    print("Part 2: Result =", sum((e.get_non_covered_surface() for e in entries)))

if __name__ == "__main__":
    solve(entries)