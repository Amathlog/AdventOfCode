import copy
from typing import List, Tuple, Dict, Optional, Set
from aoc.common.parse_entry import parse_all
from aoc.common.utils import profile
from aoc.common.grid import Grid
from aoc.common.point import Point, up, down, left, right

entries, example_entries = parse_all(__file__, "entry.txt", "example.txt")

@profile
def part_one(entry: List[str]) -> int:
    grid = Grid(entry)
    regions: Dict[str, List[Point]] = {}
    unseen_postions = set([Point(i,j) for i in range(grid.max_x) for j in range(grid.max_y)])
    while len(unseen_postions) > 0:
        start = unseen_postions.pop()
        plant = grid[start]
        if plant not in regions:
            regions[plant] = []
        
        stack = [start]
        while len(stack) > 0:
            curr = stack.pop()
            regions[plant].append(curr)
            for dir in [up, down, left, right]:
                temp = curr + dir
                if grid.is_valid(temp) and grid[temp] == plant and temp in unseen_postions:
                    unseen_postions.remove(temp)
                    stack.append(temp)

    print(regions)


@profile
def part_two(entry: List[str]) -> int:
    return 0


if __name__ == "__main__":
    print("Part 1 example:", part_one(example_entries))
    print("Part 1 entry:", part_one(entries))

    print("Part 2 example:", part_two(example_entries))
    print("Part 2 entry:", part_two(entries))
