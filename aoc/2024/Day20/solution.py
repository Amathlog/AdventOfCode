import copy
from typing import List, Tuple, Dict, Optional, Set, Any
from aoc.common.parse_entry import parse_all
from aoc.common.utils import profile
from aoc.common.astar import AStar_Solver, PriorityQueue, StatePriority
from aoc.common.grid import Grid
from aoc.common.point import Point, up, left, right, down

entries, example_entries = parse_all(__file__, "entry.txt", "example.txt")

dirs = [up, left, right, down]

class ProgramRace(AStar_Solver):
    def __init__(self, grid: Grid, start_pos: Point, end_pos: Point):
        super().__init__()
        self.grid = grid
        self.start = start_pos
        self.end = end_pos

    def heuristic(self, state: Point) -> int:
        return state.manathan_distance(self.end)
    
    def get_cost(self, state: Point) -> int:
        return 1
    
    def get_neighbors(self, state: Point) -> List[Point]:
        res = []
        for dir in dirs:
            temp = state + dir
            if self.grid.is_valid(temp) and self.grid[temp]:
                res.append(temp)
        return res
    
    def is_start(self, state: Point) -> bool:
        return state == self.start
    
    def is_end(self, state: Point) -> bool:
        return state == self.end
    
    def get_start_states(self) -> List[Point]:
        return [self.start]

@profile
def solve(entry: List[str], threshold: int, cheat_length: int) -> int:
    grid = []
    start = None
    end = None
    for i, line in enumerate(entry):
        grid.append([])
        for j, c in enumerate(line):
            if c == "#":
                grid[-1].append(False)
                continue

            if c == "S":
                start = Point(i, j)
            elif c == "E":
                end = Point(i, j)
            grid[-1].append(True)

    grid = Grid(grid)
    solver = ProgramRace(grid, start, end)
    best_path: List[Point] = solver.solve()
    benchmark = len(best_path) - 1

    best_score = {pos: i for i, pos in enumerate(best_path)}

    # Find all possible cheat positions, within a norm_1 distance of cheat length
    cheat_postions: Dict[Point, Set[Point]] = {}
    cheat_count: Dict[int, int] = {}
    for state in best_path:
        # No need to check for improvement when the best path is already below the threshold
        if benchmark - best_score[state] < threshold:
            break

        best_score_state = best_score[state]
        # No need to spend time to search outside of the grid bounds
        # Also because the full grid is covered with walls, we can even restraint the search
        # to not check those walls. (hence the 1 for min and -2 for max)
        min_x = max(1, state.x - cheat_length)
        min_y = max(1, state.y - cheat_length)
        max_x = min(grid.max_x - 2, state.x + cheat_length)
        max_y = min(grid.max_y - 2, state.y + cheat_length)

        for i in range(min_x, max_x + 1):
            for j in range(min_y, max_y + 1):
                curr = Point(i, j)
                dist = state.manathan_distance(curr)
                # We discard all the points that are farther away from the cheat length.
                if dist > cheat_length or dist == 0:
                    continue

                # If it is a wall, nothing to do
                if not grid[curr]:
                    continue

                # Otherwise, check if we improved. If we did, make sure
                # we didn't already see that cheat. If not, we found a new valid
                # pair so count it.
                tentative_best_score = best_score_state + dist
                current_best_score = best_score[curr]
                improvement = current_best_score - tentative_best_score
                if improvement >= threshold:
                    if state not in cheat_postions:
                        cheat_postions[state] = set()
                    if curr not in cheat_postions[state]:
                        cheat_postions[state].add(curr)
                        if improvement not in cheat_count:
                            cheat_count[improvement] = 0
                        cheat_count[improvement] += 1

    return sum((v for v in cheat_count.values()))


if __name__ == "__main__":
    print("Part 1 example:", solve(example_entries, 1, 2))
    print("Part 1 entry:", solve(entries, 100, 2))

    print("Part 2 example:", solve(example_entries, 50, 20))
    print("Part 2 entry:", solve(entries, 100, 20))
