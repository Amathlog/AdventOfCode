from pathlib import Path
import os
import copy
from typing import List, Tuple, Dict, Union
import sys
import time

entry_file = Path(os.path.abspath(__file__)).parent / "entry.txt"
example_file = Path(os.path.abspath(__file__)).parent / "example.txt"

class Profiling:
    def __init__(self):
        self.start = 0

    def __enter__(self):
        self.start = time.perf_counter()

    def __exit__(self, *args):
        print(f"Time taken = {(time.perf_counter() - self.start) * 1000:.2f}ms")

class Position:
    def __init__(self, x: int, y: int, z: int):
        self.x = x
        self.y = y
        self.z = z

    def min(self, other: "Position"):
        self.x = min(self.x, other.x)
        self.y = min(self.y, other.y)
        self.z = min(self.z, other.z)

    def max(self, other: "Position"):
        self.x = max(self.x, other.x)
        self.y = max(self.y, other.y)
        self.z = max(self.z, other.z)

    def __eq__(self, other: "Position") -> bool:
        return self.x == other.x and self.y == other.y and self.z == other.z

    def __hash__(self) -> int:
        return hash((self.x, self.y, self.z))

    def __repr__(self) -> str:
        return str((self.x, self.y, self.z))

    def __add__(self, other: "Position") -> "Position":
        return Position(self.x + other.x, self.y + other.y, self.z + other.z)

    def neighbors_gen(self):
        candidates = [Position(1, 0, 0), Position(-1, 0, 0), Position(0, 1, 0), Position(0, -1, 0), Position(0, 0, 1), Position(0, 0, -1)]
        for c in candidates:
            yield self + c


class LavaDroplet:
    def __init__(self, x: int, y: int, z: int):
        self.pos = Position(x, y, z)
        self.touching = 0

    def __repr__(self) -> str:
        return str(self.pos)

    def update_touching(self, others: set["LavaDroplet"]):
        for neighbor in self.pos.neighbors_gen():
            if neighbor in others:
                self.touching += 1

    def update_unreachable(self, unreachable_air: set[Tuple[int, int, int]]):
        for neighbor in self.pos.neighbors_gen():
            if neighbor in unreachable_air:
                self.touching += 1

    def get_non_covered_surface(self):
        assert self.touching <= 6
        return 6 - self.touching

    def __eq__(self, other: Union["LavaDroplet", Position]) -> bool:
        if type(other) is Position:
            return self.pos == other

        return self.pos == other.pos

    def __hash__(self) -> int:
        return hash(self.pos)

def flow3d(entries: List[LavaDroplet]):
    # Find the boundaries
    min_pos = Position(sys.maxsize, sys.maxsize, sys.maxsize)
    max_pos = Position(-99999, -99999, -99999)

    all_lava_droplets = set()

    for e in entries:
        min_pos.min(e.pos)
        max_pos.max(e.pos)
        all_lava_droplets.add(e.pos)

    # Add padding
    min_pos = min_pos + Position(-1, -1, -1)
    max_pos = max_pos + Position(1, 1, 1)

    all_air_droplets = set((Position(i,j,k) for i in range(min_pos.x, max_pos.x+1) for j in range(min_pos.y, max_pos.y+1) for k in range(min_pos.z, max_pos.z+1))).difference(all_lava_droplets)
    all_air_droplets_reachable = set()

    stack = [min_pos]

    while len(stack) != 0:
        current = stack.pop()
        if current in all_air_droplets_reachable:
            continue

        all_air_droplets_reachable.add(current)

        for c in current.neighbors_gen():
            if c.x < min_pos.x or c.x > max_pos.x or c.y < min_pos.y or c.y > max_pos.y or c.z < min_pos.z or c.z > max_pos.z:
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

        entries[i] = LavaDroplet(*tuple(int(e) for e in entries[i].split(",")))

    return entries

entries = parse_entry(entry_file)
example_entries = parse_entry(example_file)

def solve(entries: List[LavaDroplet]):
    with Profiling():
        entries_set = set(entries)
        for entry in entries:
            entry.update_touching(entries_set)

        print("Part 1: Result =", sum((e.get_non_covered_surface() for e in entries)))

    with Profiling():
        flow3d(entries)
        print("Part 2: Result =", sum((e.get_non_covered_surface() for e in entries)))

if __name__ == "__main__":
    solve(entries)