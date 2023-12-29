import copy
from typing import List, Tuple, Dict, Optional, Set
from aoc.common.parse_entry import parse_all
from aoc.common.utils import profile
from aoc.common.point import Point, intersect
import math

entries, example_entries = parse_all(__file__, "entry.txt", "example.txt")

class Hailstone:
    def __init__(self, initial_pos: Point, velocity: Point):
        self.initial_pos = initial_pos
        self.velocity = velocity

    def intersect(self, other: "Hailstone", min_test: int, max_test: int) -> bool:
        is_intersecting, impact, t, t_ = intersect(self.initial_pos, self.velocity, other.initial_pos, other.velocity)
        return is_intersecting and t >= 0 and t_ >= 0 and min_test <= impact.x <= max_test and min_test <= impact.y <= max_test

@profile
def part_one(entry: List[str], min_test: int, max_test: int) -> int:
    hailstones: List[Hailstone] = []
    for e in entry:
        pos, vel = e.split(" @ ")
        pos = pos.split(", ")
        vel = vel.split(", ")

        pos = Point(int(pos[0]), int(pos[1]))
        vel = Point(int(vel[0]), int(vel[1]))
        hailstones.append(Hailstone(pos, vel))

    count = 0
    for i in range(len(hailstones)):
        for j in range(i + 1, len(hailstones)):
            if hailstones[i].intersect(hailstones[j], min_test, max_test):
                count += 1

    return count

@profile
def part_two(entry: List[str]) -> int:
    return 0


if __name__ == "__main__":
    print("Part 1 example:", part_one(example_entries, 7, 27))
    print("Part 1 entry:", part_one(entries, 200000000000000, 400000000000000))

    print("Part 2 example:", part_two(example_entries))
    print("Part 2 entry:", part_two(entries))
