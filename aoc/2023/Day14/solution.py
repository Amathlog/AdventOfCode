import copy
from typing import List, Tuple, Dict, Optional, Set
from aoc.common.parse_entry import parse_all
from aoc.common.utils import profile
from aoc.common.grid import Grid
from aoc.common.point import Point
from enum import Enum

entries, example_entries = parse_all(__file__, "entry.txt", "example.txt")

class Direction(Enum):
    North = 0
    East = 1
    South = 2
    West = 3

class Map(Grid):
    def __init__(self, grid: List[str]):
        super().__init__(grid)
        self.obstacles_indices_col: List[List[int]] = []
        self.obstacles_indices_row: List[List[int]] = []

        self.compute_obstacles()
    
    def compute_obstacles(self):
        # First cols
        for y in range(self.max_y):
            temp = []
            for x in range(self.max_x):
                if self.get(x, y) == "#":
                    temp.append(x)
            self.obstacles_indices_col.append([-1] + temp + [self.max_y])
        
        # Then rows
        for x in range(self.max_x):
            temp = []
            for y in range(self.max_y):
                if self.get(x, y) == "#":
                    temp.append(y)
            self.obstacles_indices_row.append([-1] + temp + [self.max_x])

    def roll(self, dir: Direction):
        if dir == Direction.North or dir == Direction.South:
            for y in range(self.max_y):
                for i in range(len(self.obstacles_indices_col[y]) - 1):
                    start = self.obstacles_indices_col[y][i] + 1
                    end = self.obstacles_indices_col[y][i+1]
                    nb_rocks = sum([int(self.get(x, y) == "O") for x in range(start, end)])
                    if nb_rocks == 0:
                        continue

                    for x in range(start, end):
                        idx = x - start
                        other_idx = end - x - 1
                        if (dir == Direction.North and idx < nb_rocks) or (dir == Direction.South and other_idx < nb_rocks):
                            self.grid[x][y] = "O"
                        else:
                            self.grid[x][y] = "."
        else:
            for x in range(self.max_x):
                for i in range(len(self.obstacles_indices_row[x]) - 1):
                    start = self.obstacles_indices_row[x][i] + 1
                    end = self.obstacles_indices_row[x][i+1]
                    nb_rocks = sum([int(self.get(x, y) == "O") for y in range(start, end)])
                    if nb_rocks == 0:
                        continue

                    for y in range(start, end):
                        idx = y - start
                        other_idx = end - y - 1
                        if (dir == Direction.West and idx < nb_rocks) or (dir == Direction.East and other_idx < nb_rocks):
                            self.grid[x][y] = "O"
                        else:
                            self.grid[x][y] = "."

    def load(self):
        res = 0
        for x in range(self.max_x):
            res += (self.max_x - x) * sum([int(self.get(x, y) == "O") for y in range(self.max_y)])
        return res

    def __repr__(self) -> str:
        res = ""
        for x in range(self.max_x):
            res += "".join(self.grid[x]) + "\n"

        return res

@profile
def part_one(entry: List[str]) -> int:
    entry = [[c for c in e] for e in entry]
    my_map = Map(entry)
    my_map.roll(Direction.North)
    return my_map.load()

@profile
def part_two(entry: List[str]) -> int:
    entry = [[c for c in e] for e in entry]
    my_map = Map(entry)
    all_maps = {}
    i = 0
    while True:
        for dir in [Direction.North, Direction.West, Direction.South, Direction.East]:
            my_map.roll(dir)

        if my_map in all_maps:
            break

        all_maps[copy.deepcopy(my_map)] = i
        i += 1

    cycle = i - all_maps[my_map]
    remaining = (1000000000 - i - 1) % cycle

    for _ in range(remaining):
        for dir in [Direction.North, Direction.West, Direction.South, Direction.East]:
            my_map.roll(dir)

    return my_map.load()


if __name__ == "__main__":
    print("Part 1 example:", part_one(example_entries))
    print("Part 1 entry:", part_one(entries))

    print("Part 2 example:", part_two(example_entries))
    print("Part 2 entry:", part_two(entries))
