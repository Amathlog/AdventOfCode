from pathlib import Path
import os
import copy
from typing import List, Tuple, Dict
import sys
from enum import Enum
import numpy as np
from collections import namedtuple

entry_file = Path(os.path.abspath(__file__)).parent / "entry.txt"
example_file = Path(os.path.abspath(__file__)).parent / "example.txt"

def parse_entry(path: str) -> List[str]:
    with path.open("r") as f:
        entries = f.readlines()

    for i in range(len(entries)):
        if entries[i][-1] == '\n':
            entries[i] = entries[i][:-1]

    return entries

entries = parse_entry(entry_file)
example_entries = parse_entry(example_file)


class Direction(Enum):
    N = "^"
    E = ">"
    S = "v"
    W = "<"


dir_mapping = {
    Direction.E.value: Direction.E, 
    Direction.N.value: Direction.N, 
    Direction.S.value: Direction.S, 
    Direction.W.value: Direction.W
}


def get_incr(dir: Direction) -> "Point":
    if dir == Direction.N:
        return Point(0, -1)
    if dir == Direction.E:
        return Point(1, 0)
    if dir == Direction.S:
        return Point(0, 1)
    return Point(-1, 0)


class Point:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __add__(self, other: "Point") -> "Point":
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other: "Point") -> "Point":
        return Point(self.x - other.x, self.y - other.y)

    def __mul__(self, other: int) -> "Point":
        return Point(self.x * other, self.y * other)

    def distance(self, other: "Point") -> int:
        dist = self - other
        return abs(dist.x) + abs(dist.y)

    def __repr__(self) -> str:
        return f"({self.x}, {self.y})"

    def __eq__(self, other: "Point") -> bool:
        return self.x == other.x and self.y == other.y
    
    def __hash__(self) -> int:
        return hash((self.x, self.y))


class Blizzard:
    def __init__(self, pos: Point, dir: Direction):
        self.pos = pos
        self.dir = dir
        self.incr = get_incr(dir)
        self.inv_incr = self.incr * -1

    def move(self, grid: "Grid"):
        self.__move_internal(grid, self.incr)

    def backtrack(self, grid: "Grid"):
        self.__move_internal(grid, self.inv_incr)

    def __move_internal(self, grid: "Grid", incr: Point):
        grid[self.pos].remove(self)
        self.pos = self.pos + incr
        if grid.is_wall(self.pos):
            self.pos = self.pos + (incr * 2)
            self.pos.x %= grid.width
            self.pos.y %= grid.height
        grid[self.pos].add(self)

    def get_copy(self):
        return Blizzard(self.pos, self.dir)
        

class Grid:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.grid = [[set() for _ in range(self.width)] for _ in range(self.height)]
        self.all_blizzards = []
        self.current_state = 0

    def is_wall(self, pos: Point):
        if pos == Point(1, 0) or pos == Point(self.width - 2, self.height - 1):
            return False
        return pos.x <= 0 or pos.y <= 0 or pos.x >= self.width - 1 or pos.y >= self.height - 1

    @property
    def nb_max_states(self):
        return np.lcm(self.width, self.height)

    def get_copy(self):
        res = Grid(self.width, self.height)
        res.all_blizzards = [b.get_copy() for b in self.all_blizzards]
        for b in res.all_blizzards:
            res[b.pos].add(b)
        res.current_state = self.current_state
        return res

    def __getitem__(self, pos: Point):
        return self.grid[pos.y][pos.x]

    def to_string(self, character: Point = None) -> str:
        res = ""
        for y in range(self.height):
            for x in range(self.width):
                pos = Point(x, y)
                if character is not None and pos == character:
                    res += "E"
                    continue

                tile = self[pos]
                if self.is_wall(pos):
                    res += "#"
                elif len(tile) == 0:
                    res += "."
                elif len(tile) > 1:
                    res += str(len(tile))
                else:
                    for t in tile:
                        res += t.dir.value
            res += "\n"
        return res

    def __repr__(self) -> str:
        return self.to_string()

    @staticmethod
    def from_input(entries: List[str]) -> "Grid":
        height = len(entries)
        width = len(entries[0])
        grid = Grid(width, height)

        for y in range(height):
            for x in range(width):
                pos = Point(x, y)
                item = entries[y][x]
                if item not in ["#", "."]:
                    dir = dir_mapping[item]
                    blizzard = Blizzard(pos, dir)
                    grid[pos].add(blizzard)
                    grid.all_blizzards.append(blizzard)

        return grid

    def move_all(self):
        for blizzard in self.all_blizzards:
            blizzard.move(self)
        self.current_state += 1
        if self.current_state == self.nb_max_states:
            self.current_state = 0
        
    def backtrack_all(self):
        for blizzard in self.all_blizzards:
            blizzard.backtrack(self)
        self.current_state -= 1
        if self.current_state < 0:
            self.current_state = self.nb_max_states - 1

def generate_all_grids(grid: Grid) -> List[Grid]:
    res = [grid]
    for i in range(1, grid.nb_max_states):
        temp = res[-1].get_copy()
        temp.move_all()
        res.append(temp)
    return res


def solve(entries: List[str]) -> int:
    grid = Grid.from_input(entries)
    start = Point(1, 0)
    target = Point(grid.width - 2, grid.height - 1)

    print("Generating all grids...")
    all_grids = generate_all_grids(grid)
    print("All grids generated")

    path, final_state = dijsktra(all_grids, start, target)
    first_trip = len(path) - 2
    print(f"Part 1: Reaching the end takes at least {first_trip} minutes")

    # Then redo it twice
    path, final_state = dijsktra(all_grids, target, start, final_state)
    second_trip = len(path) - 2
    print(f"Going back to start takes at least {second_trip} minutes")

    path, final_state = dijsktra(all_grids, start, target, final_state)
    third_trip = len(path) - 2
    print(f"Going back to the end takes at least {third_trip} minutes")

    print(f"Part 2: In total {first_trip + second_trip + third_trip} minutes")

Node = namedtuple("Node", ["point", "state"])

def dijsktra(all_grids: List[Grid], start: Point, end: Point, start_state: int = 0) -> List[Point]:
    if start == end:
        return []

    width = all_grids[0].width
    height = all_grids[0].height

    nb_pos_in_grid = width * height
    nb_states = nb_pos_in_grid * len(all_grids)

    def get_id(node: Node):
        state_id = node.state * nb_pos_in_grid
        return node.point.y * width + node.point.x + state_id

    dist = [sys.maxsize for _ in range(nb_states)]
    start_node = Node(start, start_state)
    dist[get_id(start_node)] = 0
    prev = [None for _ in range(nb_states)]
    seen = set()
    to_evaluate = [start_node]
    end_state = None

    max_sort = 0

    while len(to_evaluate) > 0:
        curr: Node = to_evaluate.pop()
        pos, state = curr
        if end is not None and pos == end:
            end_state = curr
            break

        seen.add(curr)

        update = False

        next_state = (state + 1) % len(all_grids)
        next_grid = all_grids[next_state]

        neighbors = [pos + Point(1, 0), pos + Point(0, 1), pos, pos + Point(-1, 0), pos + Point(0, -1)]
        new_dist = dist[get_id(curr)] + 1

        for neighbor in neighbors:
            next = Node(neighbor, next_state)
            if next in seen:
                continue

            # We can't go into walls and blizzard
            if next_grid.is_wall(neighbor) or len(next_grid[neighbor]) > 0:
                continue

            next_id = get_id(next)
            
            if new_dist < dist[next_id]:
                dist[next_id] = new_dist
                prev[next_id] = curr
                to_evaluate.append(next)
                update = True

        if update:
            to_evaluate.sort(key=lambda x: dist[get_id(x)], reverse=True)


    if end_state is not None:
        res = [end]
        curr = end_state
        while curr is not None:
            curr_id = get_id(curr)
            res.append(prev[curr_id])
            curr = prev[curr_id]
        return res, end_state.state

    return [], 0

def simulation(grid: Grid, character: Point, target: Point, all_states: set) -> int:
    #print(grid.to_string(character))
    current_best = -1

    if character == target:
        return 0

    state = (character, grid.current_state)
    if state in all_states:
        # Already seen, backtrack
        return -1

    all_states.add(state)

    # Move all blizzards
    grid.move_all()

    # Check if we can wait
    can_wait = len(grid[character]) == 0

    # Try all actions in priority: Right, Down, Left, Up, Wait
    for incr in [Point(1, 0), Point(0, 1), Point(-1, 0), Point(0, -1)]:
        character = character + incr
        res = -1

        if character == target:
            res = 1

        # Can't go into a wall
        if not grid.is_wall(character):
            # Can't go into a blizzard
            if len(grid[character]) == 0:
                res = simulation(grid, character, target, all_states)
        
        if res != -1:
            value = res + 1
            if current_best == -1 or value < current_best:
                current_best = value

        character = character - incr
        
    if can_wait:
        res = simulation(grid, character, target, all_states)
        if res != -1:
            value = res + 1
            if current_best == -1 or value < current_best:
                current_best = value

    return current_best


if __name__ == "__main__":
    print("For example:")
    solve(example_entries)

    print("For entry:")
    solve(entries)