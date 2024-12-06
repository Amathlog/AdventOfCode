import copy
from typing import List, Tuple, Dict, Optional, Set
from aoc.common.parse_entry import parse_all
from aoc.common.utils import profile
from aoc.common.grid import Grid
from aoc.common.point import Point, up, down, left, right

entries, example_entries = parse_all(__file__, "entry.txt", "example.txt")

@profile
def solve(entry: List[str]) -> Tuple[int, int]:
    grid = Grid(entry)
    states = set()
    unique_pos = set()
    unique_obstacles = set()
    curr = None
    dir = 0
    dirs = [up, right, down, left]
    for i, line in enumerate(entry):
        for j, c in enumerate(line):
            if grid.get(i, j) == "^":
                curr = Point(i,j)
                break
        if curr is not None:
            break
    
    while True:
        states.add((curr, dir))
        unique_pos.add(curr)
        temp = curr + dirs[dir]
        if not grid.is_valid(temp):
            break

        potential_dir = (dir + 1) % len(dirs)
        if grid[temp] == "#":
            dir = potential_dir
            continue
        else:
            pass
        curr = temp

    return len(unique_pos), len(unique_obstacles)


if __name__ == "__main__":
    print("Part 1 and 2 example:", solve(example_entries))
    print("Part 1 and 2 entry:", solve(entries))
