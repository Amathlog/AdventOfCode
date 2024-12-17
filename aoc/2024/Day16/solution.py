import copy
from typing import List, Tuple, Dict, Optional, Set
from aoc.common.parse_entry import parse_all
from aoc.common.utils import profile
from aoc.common.astar import AStar_Solver
from aoc.common.grid import Grid
from aoc.common.point import Point, up, down, left, right

entries, example_entries = parse_all(__file__, "entry.txt", "example.txt")

class State:
    def __init__(self, pos: Point, dir: Point, just_turned: bool):
        self.pos = pos
        self.dir = dir
        self.just_turned = just_turned

    def __eq__(self, other: "State") -> bool:
        return self.pos == other.pos and self.dir == other.dir and self.just_turned == other.just_turned
    
    def __hash__(self) -> int:
        return hash((self.pos, self.dir, self.just_turned))
    
    def get_next_states(self, graph: Grid) -> List["State"]:
        res = []
        advance = self.pos + self.dir
        if graph.is_valid(advance) and graph[advance]:
            res.append(State(advance, self.dir, False))
        
        res.append(State(self.pos, self.dir.cross(Point(0, 0, 1)), True))
        res.append(State(self.pos, self.dir.cross(Point(0, 0, -1)), True))
        
        return res
    
    def heuristic(self, end: Point) -> int:
        goal_dir = end - self.pos
        if goal_dir.x != 0:
            goal_dir.x = -1 if goal_dir.x < 0 else 1
        if goal_dir.y != 0:
            goal_dir.y = -1 if goal_dir.y < 0 else 1

        nb_turns = self.dir.manathan_distance(goal_dir) % 2
        return self.pos.manathan_distance(end) + nb_turns * 1000
    
    def get_cost(self) -> int:
        return 1000 if self.just_turned else 1
    
    def __repr__(self) -> str:
        return str((self.pos, self.dir, self.just_turned))

class ReindeerMaze(AStar_Solver):
    def __init__(self, grid: Grid, start_pos: Point, end_pos: Point):
        super().__init__()
        self.grid = grid
        self.start = start_pos
        self.end = end_pos

    def heuristic(self, state: State) -> int:
        return state.heuristic(self.end)
    
    def get_cost(self, state: State) -> int:
        return state.get_cost()
    
    def get_neighbors(self, state: State) -> List[State]:
        return state.get_next_states(self.grid)
    
    def is_start(self, state: State) -> bool:
        return state.pos == self.start and state.dir == right and not state.just_turned
    
    def is_end(self, state: State) -> bool:
        return state.pos == self.end
    
    def get_start_states(self) -> List[State]:
        return [State(self.start, right, False)]
    
    def solve(self, find_all: bool = False) -> int:
        res = self.solve_internal(find_all)
        if not find_all:
            return sum([s.get_cost() for s in res[1:]])
        else:
            unique_pos = set([self.start, self.end])
            for path in res:
                for s in path:
                    unique_pos.add(s.pos)
            return len(unique_pos)

@profile
def part_one(entry: List[str]) -> int:
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
    return ReindeerMaze(grid, start, end).solve()

@profile
def part_two(entry: List[str]) -> int:
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
    return ReindeerMaze(grid, start, end).solve(True)


if __name__ == "__main__":
    print("Part 1 example:", part_one(example_entries))
    print("Part 1 entry:", part_one(entries))

    print("Part 2 example:", part_two(example_entries))
    print("Part 2 entry:", part_two(entries))
