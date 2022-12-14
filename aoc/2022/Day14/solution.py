from pathlib import Path
import os
import copy
from typing import List, Tuple
from enum import Enum
from collections import namedtuple

entry_file = Path(os.path.abspath(__file__)).parent / "entry.txt"
example_file = Path(os.path.abspath(__file__)).parent / "example.txt"

with entry_file.open("r") as f:
    entries = f.readlines()

for i in range(len(entries)):
    if entries[i][-1] == '\n':
        entries[i] = entries[i][:-1]


Point = namedtuple("Point", ["x", "y"])


class Type(Enum):
    Air = "."
    Rock = "#"
    Sand = "o"


class Grid:
    def __init__(self, min_x: int, max_x: int, max_y: int, infinite_ground: bool = False):
        self.min_x = min_x
        self.max_x = max_x
        self.max_y = max_y
        self.infinite_ground = infinite_ground

        if self.infinite_ground:
            # Add 2 to the y and max_y + 2 to all x
            self.max_y += 2
            self.min_x -= (self.max_y + 2)
            self.max_x += (self.max_y + 2)

        self.grid: List[List[Type]] = [[Type.Air for _ in range(self.max_x - self.min_x + 1)] for __ in range(self.max_y + 1)]

        if self.infinite_ground:
            self.add_rock_line([Point(self.min_x, self.max_y), Point(self.max_x, self.max_y)])

    def add_rock_line(self, line: List[Point]):
        for i in range(len(line) - 1):
            p1 = line[i]
            p2 = line[i+1]

            curr = Point(min(p1.x, p2.x), min(p1.y, p2.y))
            end = Point(max(p1.x, p2.x), max(p1.y, p2.y))

            p1 = curr
            p2 = end

            incr_x = ((p2.x - p1.x) // abs(p2.x - p1.x)) if p1.x != p2.x else 0
            incr_y = ((p2.y - p1.y) // abs(p2.y - p1.y)) if p1.y != p2.y else 0

            while curr.x <= end.x and curr.y <= end.y:
                self[curr] = Type.Rock
                curr = Point(curr.x + incr_x, curr.y + incr_y)

    def __setitem__(self, p: Point, t: Type):
        self.grid[p.y][p.x - self.min_x] = t

    def __getitem__(self, p: Point):
        return self.grid[p.y][p.x - self.min_x]

    def is_valid_pos(self, p: Point):
        return p.x >= self.min_x and p.x <= self.max_x and p.y >= 0 and p.y <= self.max_y

    def add_sand(self, start_pos = Point(500, 0)) -> bool:
        curr = start_pos
        if self[start_pos] != Type.Air:
            return False

        while True:
            found_air = False
            pos_to_test = [Point(curr.x, curr.y + 1), Point(curr.x - 1, curr.y + 1), Point(curr.x + 1, curr.y + 1)]
            for tentative in pos_to_test:
                if not self.is_valid_pos(tentative):
                    return False
                
                if self[tentative] == Type.Air:
                    curr = tentative
                    found_air = True
                    break

            if not found_air:
                self[curr] = Type.Sand
                return True


    def __repr__(self) -> str:
        res = ""
        for l in self.grid:
            for t in l:
                res += t.value
            res += "\n"

        return res

    @staticmethod
    def from_input(input: List[str], infinite_ground: bool = False) -> "Grid":
        all_lines: List[List[Point]] = []
        min_x = 99999999
        max_x = -99999999
        max_y = -99999999

        for e in input:
            line = e.split(" -> ")
            line = [Point(*[int(x) for x in p.split(",")]) for p in line]
            all_lines.append(line)

            all_x = [p.x for p in line]
            all_y = [p.y for p in line]

            min_x = min([min_x] + all_x)
            max_x = max([max_x] + all_x)
            max_y = max([max_y] + all_y)

        grid = Grid(min_x, max_x, max_y, infinite_ground)

        for line in all_lines:
            grid.add_rock_line(line)

        return grid

if __name__ == "__main__":
    grid = Grid.from_input(entries)
    i = 0
    while grid.add_sand():
        i += 1

    print(grid)
    print("Part 1: Number of unit of sand rested =", i)

    grid2 = Grid.from_input(entries, True)
    i = 0

    while grid2.add_sand():
        i += 1

    print(grid2)
    print("Part 2: Number of unit of sand rested with infinite ground =", i)
