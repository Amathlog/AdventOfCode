from collections import defaultdict
import copy
from typing import List, Tuple, Dict, Optional, Set
from aoc.common.parse_entry import parse_all
from aoc.common.utils import profile
from aoc.common.grid import Grid, Point

entries, example_entries = parse_all(__file__, "entry.txt", "example.txt")

@profile
def part_one(entry: List[str]) -> int:
    grid = Grid(entry)
    beams = {Point(0, entry[0].find("S"))}
    split = 0
    for i in range(1, len(entry)-1):
        new_beams = set()
        for b in beams:
            b += Point(1, 0)
            if grid[b] == "^":
                split += 1
                new_beams.add(b + Point(0, -1))
                new_beams.add(b + Point(0, 1))
            else:
                new_beams.add(b)
        beams = new_beams

    return split

@profile
def part_two(entry: List[str]) -> int:
    grid = Grid(entry)
    beams = {Point(0, entry[0].find("S")): 1}

    for i in range(1, len(entry)-1):
        new_beams = defaultdict(int)
        for b, v in beams.items():
            b += Point(1, 0)
            if grid[b] == "^":
                new_beams[b + Point(0, -1)] += v
                new_beams[b + Point(0, 1)] += v
            else:
                new_beams[b] += v
        beams = new_beams

    return sum(beams.values())


if __name__ == "__main__":
    print("Part 1 example:", part_one(example_entries))
    print("Part 1 entry:", part_one(entries))

    print("Part 2 example:", part_two(example_entries))
    print("Part 2 entry:", part_two(entries))
