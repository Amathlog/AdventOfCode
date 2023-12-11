from pathlib import Path
import os
import copy
from typing import List, Tuple, Dict
from aoc.common.parse_entry import parse_all
from aoc.common.point import Point

entries, example_entries = parse_all(__file__, "entry.txt", "example.txt")

class Map:
    def __init__(self, entry: List[str], expansion: int):
        self.galaxies: List[Point] = []

        self.compute_galaxies(entry, expansion)

    def compute_galaxies(self, entry: List[str], expansion: int) -> None:
        rows = [False] * len(entry)
        cols = [False] * len(entry[0])
        for i in range(len(entry)):
            for j in range(len(entry[0])):
                if entry[i][j] == ".":
                    continue

                rows[i] = True
                cols[j] = True
                self.galaxies.append(Point(i, j))

        offset = 0
        for i, row in enumerate(rows):
            if not row:
                for galaxy in self.galaxies:
                    if galaxy.x - offset > i:
                        galaxy.x += expansion
                offset += expansion

        offset = 0        
        for j, col in enumerate(cols):
            if not col:
                for galaxy in self.galaxies:
                    if galaxy.y - offset > j:
                        galaxy.y += expansion
                offset += expansion


def part_one(entry: List[str]) -> int:
    my_map = Map(entry, 1)
    res = 0
    for i, galaxy_a in enumerate(my_map.galaxies):
        for j, galaxy_b in enumerate(my_map.galaxies[i+1:]):
            dist = galaxy_a.manathan_distance(galaxy_b)
            res += dist
    return res


def part_two(entry: List[str]) -> int:
    my_map = Map(entry, 1000000 - 1)
    res = 0
    for i, galaxy_a in enumerate(my_map.galaxies):
        for j, galaxy_b in enumerate(my_map.galaxies[i+1:]):
            dist = galaxy_a.manathan_distance(galaxy_b)
            res += dist
    return res


if __name__ == "__main__":
    print("Part 1 example:", part_one(example_entries))
    print("Part 1 entry:", part_one(entries))

    print("Part 2 example:", part_two(example_entries))
    print("Part 2 entry:", part_two(entries))

