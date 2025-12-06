import copy
from typing import List, Tuple, Dict, Optional, Set
from aoc.common.parse_entry import parse_all
from aoc.common.utils import profile
from aoc.common.grid import Grid, Point

entries, example_entries = parse_all(__file__, "entry.txt", "example.txt")

@profile
def part_one(entry: List[str]) -> int:
    grid = Grid(entry)
    res = 0
    for x in range(grid.max_x):
        for y in range(grid.max_y):
            if grid.get(x,y) != '@':
                continue

            count = 0
            for incr_x in (-1, 0, 1):
                for incr_y in (-1, 0, 1):
                    p = Point(x + incr_x, y + incr_y)
                    if (p.x == x and p.y == y) or not grid.is_valid(p):
                        continue

                    if grid[p] == '@':
                        count += 1
            
            if count < 4:
                res += 1
    return res

@profile
def part_two(entry: List[str]) -> int:
    entry = [[1 if c == '@' else 0 for c in e] for e in entry] 
    grid = Grid.as_int_grid(entry)
    res = 0
    while True:
        to_be_removed = []
        for x in range(grid.max_x):
            for y in range(grid.max_y):
                if grid.get(x,y) != 1:
                    continue

                count = 0
                for incr_x in (-1, 0, 1):
                    for incr_y in (-1, 0, 1):
                        p = Point(x + incr_x, y + incr_y)
                        if (p.x == x and p.y == y) or not grid.is_valid(p):
                            continue

                        if grid[p] == 1:
                            count += 1
                
                if count < 4:
                    res += 1
                    to_be_removed.append(Point(x, y))

        if len(to_be_removed) == 0:
            break

        for p in to_be_removed:
            grid[p] = 0
                    
    return res


if __name__ == "__main__":
    print("Part 1 example:", part_one(example_entries))
    print("Part 1 entry:", part_one(entries))

    print("Part 2 example:", part_two(example_entries))
    print("Part 2 entry:", part_two(entries))
