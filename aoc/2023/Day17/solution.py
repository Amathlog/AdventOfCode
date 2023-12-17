import copy
from typing import Any, List, Tuple, Dict, Optional, Set
from aoc.common.parse_entry import parse_all
from aoc.common.utils import profile
from aoc.common.grid import Grid
from aoc.common.grid import Point
from aoc.common.direction import *
from queue import PriorityQueue
from aoc.common.astar import AStar_Solver

entries, example_entries = parse_all(__file__, "entry.txt", "example.txt")


class State:
    min_straight = 0
    max_straight = 3
    def __init__(self, pos: Point, dir: Direction, straight: int):
        self.pos = pos
        self.dir = dir
        self.straight = straight
        assert(self.straight < State.max_straight)

    def __eq__(self, other: "State") -> bool:
        return self.pos == other.pos and self.dir == other.dir and self.straight == other.straight
    
    def __hash__(self) -> int:
        return hash((self.pos, self.dir, self.straight))
    
    def get_next_states(self, graph: Grid) -> List["State"]:
        left_state = None
        right_state = None
        if (self.straight >= State.min_straight - 1):
            left_turn = turn_counterclockwise(self.dir, 90)
            right_turn = turn_clockwise(self.dir, 90)

            left_state = State(advance(self.pos, left_turn), left_turn, 0)
            right_state = State(advance(self.pos, right_turn), right_turn, 0)

        if self.straight < State.max_straight - 1:
            straight_state = State(advance(self.pos, self.dir), self.dir, self.straight + 1)
        else:
            straight_state = None

        res = []
        for s in (left_state, right_state, straight_state):
            if s is None or not graph.is_valid(s.pos):
                continue
            res.append(s)
        
        return res
    
    def __repr__(self) -> str:
        return str((self.pos, self.dir, self.straight))


class ClumsyCrucible(AStar_Solver):
    def __init__(self, grid: List[str]):
        super().__init__()
        self.grid = Grid([[int(y) for y in x] for x in grid])
        self.end = Point(self.grid.max_x - 1, self.grid.max_y - 1)

    def heuristic(self, state: State) -> int:
        return state.pos.manathan_distance(self.end)
    
    def get_cost(self, state: State) -> int:
        return self.grid[state.pos]
    
    def get_neighbors(self, state: Any) -> List[Any]:
        return state.get_next_states(self.grid)
    
    def is_start(self, state: Any) -> bool:
        return state.pos == Point(0, 0)
    
    def is_end(self, state: Any) -> bool:
        return state.pos == self.end
    
    def get_start_states(self) -> List[State]:
        return [State(Point(0, 0), Direction.East, 0), State(Point(0, 0), Direction.South, 0)]
    
    def solve(self) -> Any:
        res = self.solve_internal()
        return sum([self.grid[s.pos] for s in res[1:]])


@profile
def part_one(entry: List[str]) -> int:
    graph = ClumsyCrucible(entry)
    return graph.solve()


@profile
def part_two(entry: List[str]) -> int:
    State.min_straight = 4
    State.max_straight = 10
    graph = ClumsyCrucible(entry)
    return graph.solve()


if __name__ == "__main__":
    print("Part 1 example:", part_one(example_entries))
    print("Part 1 entry:", part_one(entries))

    print("Part 2 example:", part_two(example_entries))
    print("Part 2 entry:", part_two(entries))
