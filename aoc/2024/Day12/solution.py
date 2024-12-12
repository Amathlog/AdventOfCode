import copy
from typing import List, Tuple, Dict, Optional, Set
from aoc.common.parse_entry import parse_all
from aoc.common.utils import profile
from aoc.common.grid import Grid
from aoc.common.point import Point, up, down, left, right

entries, example_entries = parse_all(__file__, "entry.txt", "example.txt")

dirs = {up: 0, down: 1, left: 2, right: 3}

class Plant:
    side_number = 0
    def __init__(self, name: str, pos: Point):
        self.name = name
        self.pos = pos
        self.boundaries = [False] * 4

    def add_boundary(self, dir: Point):
        self.boundaries[dirs[dir]] = True


@profile
def solve(entry: List[str]) -> int:
    grid = Grid([[Plant(entry[i][j], Point(i,j)) for j in range(len(entry[i]))] for i in range(len(entry))])
    regions: Dict[str, List[List[Plant]]] = {}

    # Flood-fill
    # While we have unseen positions, pop the first element. It is a new region.
    # Then for each position, look around. If they are the same name, they are in the same region, so add it to 
    # the list of positions to check, only if we haven't checked it yet.
    # Otherwise, if it is outside of the grid or not the same name, it is a boundary, so mark it as boundary.
    # The perimeter will be the sum of all the boundaries.
    unseen_postions = set([Point(i,j) for i in range(grid.max_x) for j in range(grid.max_y)])
    while len(unseen_postions) > 0:
        start = unseen_postions.pop()
        plant_name = grid[start].name
        if plant_name not in regions:
            regions[plant_name] = []
        
        regions[plant_name].append([])
        
        stack = [grid[start]]
        while len(stack) > 0:
            curr = stack.pop()
            regions[plant_name][-1].append(curr)
            for dir in dirs.keys():
                temp = curr.pos + dir
                if grid.is_valid(temp) and grid[temp].name == plant_name:
                    if temp in unseen_postions:
                        unseen_postions.remove(temp)
                        stack.append(grid[temp])
                else:
                    curr.add_boundary(dir)

    result_part1 = 0
    result_part2 = 0
    for rs in regions.values():
        for r in rs:
            area = len(r)
            # To determine all the sides, we do a 1D flood-fill, using the cross with Z up and down to get the perpendicular directions of the boundaries.
            # We put all the points with a boundary in a set of tuple: (pos, boundary_dir)
            # We pop the first element, it will be a new side, then we go perpendicular in both directions until we reach the limit, removing the seen elements on the go.
            unseen_boundaries: Set[Tuple[Point, Point]] = set()
            side_number = 0
            for plant in r:
                for dir in dirs.keys():
                    if plant.boundaries[dirs[dir]]:
                        unseen_boundaries.add((plant.pos, dir))

            perimeter = len(unseen_boundaries)
            result_part1 += area * perimeter
            
            while len(unseen_boundaries) > 0:
                start, dir = unseen_boundaries.pop()
                side_number += 1
                for perpendicular_dir in [dir.cross(Point(0, 0, 1)), dir.cross(Point(0, 0, -1))]:
                    curr = start + perpendicular_dir
                    while (curr, dir) in unseen_boundaries:
                        unseen_boundaries.remove((curr, dir))
                        curr = curr + perpendicular_dir

            result_part2 += area * side_number

    return result_part1, result_part2


if __name__ == "__main__":
    print("Part 1 and 2 example:", solve(example_entries))
    print("Part 1 and 2 entry:", solve(entries))
