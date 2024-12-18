import copy
from typing import List, Tuple, Dict, Optional, Set
from aoc.common.parse_entry import parse_all
from aoc.common.utils import profile
from aoc.common.grid import Grid
from aoc.common.point import Point, up, down, left, right
from aoc.common.astar import AStar_Solver

entries, example_entries = parse_all(__file__, "entry.txt", "example.txt")

class CorruptedBytes(AStar_Solver):
    def __init__(self, corrupted: Set[Point], start_pos: Point, end_pos: Point):
        super().__init__()
        self.corrupted = corrupted
        self.start = start_pos
        self.end = end_pos

    def heuristic(self, state: Point) -> int:
        return state.manathan_distance(self.end)
    
    def get_cost(self, state: Point) -> int:
        return 1
    
    def get_neighbors(self, state: Point) -> List[Point]:
        res = []
        for dir in [up, down, left, right]:
            temp = state + dir
            if temp in self.corrupted or temp.x < 0 or temp.y < 0 or temp.x > self.end.x or temp.y > self.end.y:
                continue
            res.append(temp)
        return res
    
    def is_start(self, state: Point) -> bool:
        return state == self.start
    
    def is_end(self, state: Point) -> bool:
        return state == self.end
    
    def get_start_states(self) -> List[Point]:
        return [self.start]
    
def print_grid(corrupted: Set[Point], end: Point, path: Set[Point]):
    res = ""
    for i in range(end.x+1):
        for j in range(end.y+1):
            p = Point(i, j)
            if p in corrupted:
                res += "#"
            elif p in path:
                res += "O"
            else:
                res += "."
        res += "\n"
    print(res)

@profile
def solve(entry: List[str], start: int) -> int:
    all_bytes = []
    corrupted_bytes = set()
    end_pos = Point(0, 0)

    def add_corrupted(line: str):
        y, x = line.split(",")
        new_byte = Point(int(x), int(y))
        corrupted_bytes.add(new_byte)
        all_bytes.append(new_byte)
        if new_byte.x > end_pos.x:
            end_pos.x = new_byte.x
        if new_byte.y > end_pos.y:
            end_pos.y = new_byte.y
    
    for line in entry[:start]:
        add_corrupted(line)

    start_pos = Point(0, 0)
    i = start
    previous_end_pos = copy.deepcopy(end_pos)
    previous_path = set(CorruptedBytes(corrupted_bytes, start_pos, end_pos).solve())
    res_part1 = len(previous_path) - 1
    while True:
        add_corrupted(entry[i])
        # Only need to re-run the algorithm if the new byte cuts our shortest path (or the end pos changed, which change the size of the grid)
        if all_bytes[i] in previous_path or previous_end_pos != end_pos:
            new_path = CorruptedBytes(corrupted_bytes, start_pos, end_pos).solve()

            if len(new_path) == 0:
                break

            previous_path = set(new_path)
            previous_end_pos = copy.deepcopy(end_pos)

        i += 1
    
    return res_part1, entry[i]


if __name__ == "__main__":
    print("Part 1 and 2 example:", solve(example_entries, 12))
    print("Part 1 and 2 entry:", solve(entries, 1024))
