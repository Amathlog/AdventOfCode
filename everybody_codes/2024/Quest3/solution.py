import copy
from typing import List, Tuple, Dict, Optional, Set
from aoc.common.parse_entry import parse_all_multiple_parts, default_separator
from aoc.common.utils import profile
from aoc.common.grid import Grid, Point

entries, example_entries = parse_all_multiple_parts(__file__, default_separator, 3, "entry.txt", "example.txt")

up = Point(-1, 0)
down = Point(1, 0)
left = Point(0, -1)
right = Point(0, 1)

@profile
def solve(entry: List[str], diag: bool = False) -> int:
    dirs = [up, down, left, right] if not diag else [up, down, left, right, up + left, up + right, down + left, down + right]
    possible_positions: List[Point] = []
    grid = []
    for i, line in enumerate(entry):
        grid.append([])
        for j, c in enumerate(line):
            value = 0 if c == '.' else 1
            grid[-1].append(value)
            if value == 1:
                possible_positions.append(Point(i, j))

    grid = Grid(grid)
    result = len(possible_positions)
    while len(possible_positions) > 0:
        #print(grid.pretty_str())
        new_grid = copy.deepcopy(grid)
        new_possible_positions = []
        while len(possible_positions) != 0:
            curr = possible_positions.pop()
            count = 0
            for dir in dirs:
                new_pos = curr + dir
                value = grid[new_pos] if grid.is_valid(new_pos) else 0
                if value != grid[curr]:
                    break
                count += 1
            
            if count == len(dirs):
                new_grid[curr] += 1
                new_possible_positions.append(curr)
                result += 1

        grid = new_grid
        possible_positions = new_possible_positions
    
    return result

if __name__ == "__main__":
    print("Part 1 example:", solve(example_entries[0]))
    print("Part 1 entry:", solve(entries[0]))

    print("Part 2 example:", solve(example_entries[1]))
    print("Part 2 entry:", solve(entries[1]))

    print("Part 3 example:", solve(example_entries[2], True))
    print("Part 3 entry:", solve(entries[2], True))
