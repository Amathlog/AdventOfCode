import copy
from typing import List, Tuple, Dict, Optional, Set
from aoc.common.parse_entry import parse_all
from aoc.common.utils import profile
from aoc.common.grid import Grid
from aoc.common.point import Point, up, down, left, right

entries, example_entries = parse_all(__file__, "entry.txt", "example.txt")

dirs = [up, right, down, left]

def simulate_with_new_obstacle(start: Point, dir: int, grid: Grid, seen_states: Set, new_obstacle: Point):
    states = set()
    got_out = False
    curr = start
    while True:
        state = (curr, dir)
        if state in states or state in seen_states:
            break

        states.add(state)
        temp = curr + dirs[dir]
        if not grid.is_valid(temp):
            got_out = True
            break

        if grid[temp] == "#" or temp == new_obstacle:
            dir = (dir + 1) % len(dirs)
            continue

        curr = temp

    return got_out

@profile
def solve(entry: List[str]) -> Tuple[int, int]:
    grid = Grid(entry)
    states = set()
    unique_pos = set()
    unique_obstacles = set()
    curr = None
    dir = 0
    
    for i, line in enumerate(entry):
        for j, c in enumerate(line):
            if c == "^":
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
        elif temp not in unique_pos:
            if not simulate_with_new_obstacle(curr, potential_dir, grid, states, temp):
                unique_obstacles.add(temp)
    
        curr = temp

    return len(unique_pos), len(unique_obstacles)


if __name__ == "__main__":
    print("Part 1 and 2 example:", solve(example_entries))
    print("Part 1 and 2 entry:", solve(entries))
