import copy
from typing import Any, List, Tuple, Dict, Optional, Set
from aoc.common.parse_entry import parse_all
from aoc.common.utils import profile
from aoc.common.astar import AStar_Solver
from aoc.common.grid import Grid
from aoc.common.point import Point
from aoc.common.direction import *
import math

entries, example_entries = parse_all(__file__, "entry.txt", "example.txt")

class Tile:
    index = 0
    def __init__(self, c: str, slip: bool) -> None:
        self.walkable = c != "#"
        self.direction = None
        if self.walkable:
            self.index = Tile.index
            Tile.index += 1
            if slip:
                if c == ">":
                    self.direction = Direction.East
                elif c == "<":
                    self.direction = Direction.West
                elif c == "^":
                    self.direction = Direction.North
                elif c == "v":
                    self.direction = Direction.South

class Map(Grid):
    def __init__(self, grid: List[str], slip: bool) -> None:
        Tile.index = 0
        super().__init__([[Tile(c, slip) for c in e] for e in grid])
        self.walkable_num = Tile.index

class BitField:
    def __init__(self, size: int):
        self.size = size
        self.field = [0] * math.ceil(self.size / 64)

    def set(self, bit: int):
        assert(bit < self.size)
        index = bit >> 6
        bit_n = bit & 0x3f
        self.field[index] |= (1 << bit_n)

    def reset(self, bit: int):
        assert(bit < self.size)
        index = bit >> 6
        bit_n = bit & 0x3f
        self.field[index] &= ~(1 << bit_n)

    def is_set(self, bit: int):
        assert(bit < self.size)
        index = bit >> 6
        bit_n = bit & 0x3f
        return (self.field[index] & (1 << bit_n)) != 0

    def __hash__(self) -> int:
        res = 0
        for word in self.field:
            res ^= word
        return res
    
    def __eq__(self, other: "BitField") -> bool:
        return self.field == other.field

def get_next_states(pos: Point, direction: Direction, graph: Map) -> List[Point]:
    tile = graph[pos]
    reverse_dir = turn_clockwise(direction, 180)
    assert(tile.walkable)
    if tile.direction is not None:
        if tile.direction == reverse_dir:
            return []
        else:
            return [(advance(pos, tile.direction), tile.direction)]

    res = []
    for dir in [Direction.East, Direction.West, Direction.North, Direction.South]:
        # Can't go back
        if dir == reverse_dir:
            continue

        new_pos = advance(pos, dir)
        if not graph.is_valid(new_pos) or not graph[new_pos].walkable:
            continue
    
        res.append((new_pos, dir))
    return res

def backtrack(start_pos: Point, end_pos: Point, graph: Map) -> List[Point]:
    already_seen = {}
    current_bitfield = BitField(graph.walkable_num)

    return backtrack_internal(start_pos, Direction.South, end_pos, graph, 0, already_seen, current_bitfield)

def backtrack_internal(curr: Point, dir: Direction, end_pos: Point, graph: Map, curr_length, already_seen, current_bitfield) -> List[Point]:
    if curr == end_pos:
        return [end_pos]

    state = (curr, current_bitfield)
    if (curr, current_bitfield) in already_seen:
        return None
    
    already_seen[(curr, copy.deepcopy(current_bitfield))] = True
    
    tile = graph[curr]
    current_bitfield.set(tile.index)

    max_length = 0
    max_path = None

    for next_pos, dir in get_next_states(curr, dir, graph):
        if current_bitfield.is_set(graph[next_pos].index):
            continue

        path = backtrack_internal(next_pos, dir, end_pos, graph, curr_length+1, already_seen, current_bitfield)
        if path is None:
            continue

        if curr_length + len(path) > max_length:
            max_length = curr_length + len(path)
            max_path = [curr] + path

    current_bitfield.reset(tile.index)
    return max_path


@profile
def part_one(entry: List[str]) -> int:
    graph = Map(entry, True)
    for i, tile in enumerate(graph.grid[0]):
        if tile.walkable:
            start_point = Point(0, i)

    for i, tile in enumerate(graph.grid[-1]):
        if tile.walkable:
            end_point = Point(graph.max_x - 1, i)
    
    return len(backtrack(start_point, end_point, graph)) - 1

@profile
def part_two(entry: List[str]) -> int:
    graph = Map(entry, False)
    for i, tile in enumerate(graph.grid[0]):
        if tile.walkable:
            start_point = Point(0, i)

    for i, tile in enumerate(graph.grid[-1]):
        if tile.walkable:
            end_point = Point(graph.max_x - 1, i)
    
    return len(backtrack(start_point, end_point, graph)) - 1


if __name__ == "__main__":
    import sys
    sys.setrecursionlimit(10000) 
    print("Part 1 example:", part_one(example_entries))
    #print("Part 1 entry:", part_one(entries))

    print("Part 2 example:", part_two(example_entries))
    print("Part 2 entry:", part_two(entries))
