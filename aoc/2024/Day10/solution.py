import copy
from typing import List, Tuple, Dict, Optional, Set
from aoc.common.parse_entry import parse_all
from aoc.common.utils import profile
from aoc.common.grid import Grid
from aoc.common.point import Point, up, down, left, right

entries, example_entries = parse_all(__file__, "entry.txt", "example.txt")

@profile
def part_one(entry: List[str]) -> int:
    grid = Grid.as_int_grid(entry)

    seen_positions = {}
    start_positions = []
    for i in range(grid.max_x):
        for j in range(grid.max_y):
            if grid.get(i, j) == 0:
                start_positions.append(Point(i, j))

    def recurse(curr: Point):
        if curr in seen_positions:
            return seen_positions[curr]
        
        if grid[curr] == 9:
            return {curr}
        
        seen_positions[curr] = set()

        for dir in [up, down, left, right]:
            temp = curr + dir
            if grid.is_valid(temp) and grid[temp] == grid[curr] + 1:
                seen_positions[curr].update(recurse(temp))

        return seen_positions[curr]
    
    results = map(recurse, start_positions)
    
    return sum(map(len, results))

@profile
def part_two(entry: List[str]) -> int:
    grid = Grid.as_int_grid(entry)

    seen_positions = {}
    start_positions = []
    for i in range(grid.max_x):
        for j in range(grid.max_y):
            if grid.get(i, j) == 0:
                start_positions.append(Point(i, j))

    def recurse(curr: Point):
        if curr in seen_positions:
            return seen_positions[curr]
        
        if grid[curr] == 9:
            return 1
        
        seen_positions[curr] = 0

        for dir in [up, down, left, right]:
            temp = curr + dir
            if grid.is_valid(temp) and grid[temp] == grid[curr] + 1:
                seen_positions[curr] += recurse(temp)

        return seen_positions[curr]
    
    results = map(recurse, start_positions)
    
    return sum(results)


if __name__ == "__main__":
    print("Part 1 example:", part_one(example_entries))
    print("Part 1 entry:", part_one(entries))

    print("Part 2 example:", part_two(example_entries))
    print("Part 2 entry:", part_two(entries))
