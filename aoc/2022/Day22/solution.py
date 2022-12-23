from pathlib import Path
import os
import copy
from typing import List, Tuple, Dict, Optional, Callable
from enum import Enum
import re

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


class Type(Enum):
    Empty = 0
    Wall = 1
    Teleport = 2
    Void = 3


class Direction(Enum):
    Left = 0
    Up = 1
    Right = 2
    Down = 3


def get_direction(pos: "Point") -> Direction:
    if pos.x > 0:
        return Direction.Right
    if pos.x < 0:
        return Direction.Left
    if pos.y > 0:
        return Direction.Down

    return Direction.Up

def get_incr(dir: Direction) -> "Point":
    if dir == Direction.Left:
        return Point(-1, 0)
    if dir == Direction.Right:
        return Point(1, 0)
    if dir == Direction.Down:
        return Point(0, 1)
    return Point(0, -1)

def get_opposite_direction(pos: "Point") -> Direction:
    return get_direction(pos * -1)


def transform(pos: "Point", initial_dir: Direction, initial_origin: "Point", new_dir: Direction, new_origin: "Point", zone_size: int) -> "Point":
    transform_number = (initial_dir.value - new_dir.value) % 4
    if transform_number == 2:
        # Nothing to do
        return pos
    if transform_number == 0:
        return Point(new_origin.x - (pos.x - initial_origin.x), new_origin.y)
    if transform_number == 1: # Turned left
        return Point()
    if transform_number == 3: # Turned right
        return Point()

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


class Tile:
    def __init__(self, pos: Point, _type: Type, zone_size: int):
        self.set_type(_type)
        self.pos = pos
        # Follow "Direction" enum index order
        self.teleport_coordinates: List[Point] = [None] * 4
        self.visited: bool = False
        self.visited_twice: bool = False
        self.current_zone = None
        self.zone_size = zone_size

    def set_type(self, _type: Type):
        self.type = _type
        # Follow "Direction" enum index order
        self.distance_to_wall: List[int] = [None] * 4 if _type != Type.Wall else [0] * 4
        self.distance_to_teleport: List[int] = [None] * 4 if _type != Type.Teleport else [0] * 4

    def clear_teleport_cache(self):
        self.visited = False
        self.visited_twice = False
        self.distance_to_teleport = [None] * 4 if self.type != Type.Teleport else [0] * 4

    def update_teleport_part1(self, grid: "Grid"):
        # Find all Empty around
        valid_neighbors = []
        for neighbor in grid.neighbor_incr_gen(self.pos, safe=True):
            if grid[self.pos + neighbor].type == Type.Empty:
                valid_neighbors.append(neighbor)

        # Then find the opposite teleport
        for neighbor in valid_neighbors:
            curr = grid[self.pos + neighbor]
            previous_was_wall = False
            while curr.type != Type.Teleport:
                previous_was_wall = curr.type == Type.Wall
                curr = grid[curr.pos + neighbor]
            
            # When we reach another teleport, we need to make sure there was not a wall just
            # next to it. If so, count the current teleport as a wall
            initial_dir = get_opposite_direction(neighbor)
            if previous_was_wall:
                self.distance_to_wall[initial_dir.value] = 0
            else:
                self.teleport_coordinates[initial_dir.value] = curr.pos - neighbor

    def get_current_zone(self, grid: "Grid"):
        if self.current_zone is None:
            column_id = (self.pos.x - 1) // self.zone_size
            row_id = (self.pos.y - 1) // self.zone_size
            self.current_zone = grid.zones[(column_id, row_id)]

        return self.current_zone

    def update_teleport_part2(self, grid: "Grid"):
        # Find all Empty around
        valid_neighbors = []
        for neighbor in grid.neighbor_incr_gen(self.pos, safe=True):
            if grid[self.pos + neighbor].type == Type.Empty:
                valid_neighbors.append(neighbor)

        # Then find the opposite teleport
        for neighbor in valid_neighbors:
            curr = grid[self.pos + neighbor]
            curr_zone = curr.get_current_zone(grid)

                
    def update_cache(self, grid: "Grid", second_time: bool = False, folded: bool = False):
        if self.visited and (not second_time or self.visited_twice):
            return

        self.visited = True
        if second_time:
            self.visited_twice = True

        if self.type == Type.Wall:
            return

        elif self.type == Type.Teleport and not second_time:
            if folded:
                self.update_teleport_part2(grid)
            else:
                self.update_teleport_part1(grid)            
        else:
            for neighbor, dir in grid.neighbor_points_gen(self.pos, safe=True, with_dir=True):
                neighbor_tile = grid[neighbor]
                if neighbor_tile.distance_to_wall[dir.value] is not None and self.distance_to_wall[dir.value] is None:
                    self.distance_to_wall[dir.value] = neighbor_tile.distance_to_wall[dir.value] + 1

                if neighbor_tile.distance_to_teleport[dir.value] is not None and self.distance_to_teleport[dir.value] is None:
                    self.distance_to_teleport[dir.value] = neighbor_tile.distance_to_teleport[dir.value] + 1


class Grid:
    def __init__(self, width: int, height: int, zones, zone_mapping):
        self.width = width
        self.height = height
        self.zone_size = (max((width, height)) - 2) // 4
        self.grid = [[Tile(Point(i,j), Type.Void, self.zone_size) for i in range(self.width)] for j in range(self.height)]
        self.topleft_pos = None
        self.zones: Dict[Tuple[int, int], int] = zones
        self.zone_mapping: List[List[Callable, Direction]] = zone_mapping

    def __getitem__(self, pos: Point) -> Tile:
        assert pos.x >= 0 and pos.x < self.width and pos.y >= 0 and pos.y < self.height
        return self.grid[pos.y][pos.x]

    def neighbor_points_gen(self, origin: Point, safe: bool, with_dir: bool) -> Point:
        for incr in self.neighbor_incr_gen(origin, safe):
            if with_dir:
                yield origin + incr, get_direction(incr)
            else:
                yield origin + incr

    def neighbor_incr_gen(self, origin: Point, safe: bool) -> Point:
        for incr in [Point(-1, 0), Point(0, -1), Point(1, 0), Point(0, 1)]:
            neighbor = origin + incr
            if safe and (neighbor.x < 0 or neighbor.y < 0 or neighbor.x >= self.width or neighbor.y >= self.height):
                continue
            yield incr

    def update_cache(self, folded: bool = False):
        for j in range(self.height):
            for i in range(self.width):
                tile = self.grid[j][i]
                tile.update_cache(self, folded)

        for j in reversed(range(self.height)):
            for i in reversed(range(self.width)):
                tile = self.grid[j][i]
                tile.update_cache(self, second_time=True, folded=folded)
                if tile.type == Type.Empty:
                    # Validate that all directions are valid
                    for dir in range(4):
                        assert tile.distance_to_wall[dir] is not None or tile.distance_to_teleport[dir] is not None
                        assert tile.distance_to_wall[dir] is None or tile.distance_to_wall[dir] >= 0
                        assert tile.distance_to_teleport[dir] is None or tile.distance_to_teleport[dir] >= 0

    def clear_teleport_cache(self):
        for j in range(self.height):
            for i in range(self.width):
                self.grid[j][i].clear_teleport_cache()

    @staticmethod
    def from_input(input: List[str], zones, zone_mapping) -> "Grid":
        # + 2 for padding
        height = len(input) + 2
        width = max((len(i) for i in input)) + 2

        grid = Grid(width, height, zones, zone_mapping)
        for j in range(1, height - 1):
            for i in range(1, width - 1):
                pos = Point(i, j)
                input_pos = Point(i - 1, j - 1)
                if input_pos.x >= len(input[input_pos.y]):
                    continue

                not_void = False
                if input[input_pos.y][input_pos.x] == "#":
                    grid[pos].set_type(Type.Wall)
                    not_void = True
                elif input[input_pos.y][input_pos.x] == ".":
                    grid[pos].set_type(Type.Empty)
                    not_void = True
                    if grid.topleft_pos is None:
                        grid.topleft_pos = pos
                    
                if not_void:
                    # Also check around, to create teleports
                    # With padding, we are safe
                    for neighbor in grid.neighbor_points_gen(pos, safe=False, with_dir=False):
                        input_neighbor = neighbor - Point(1, 1)

                        if neighbor.x == 0 or neighbor.y == 0 or neighbor.x == width - 1 or neighbor.y == height - 1:
                            grid[neighbor].set_type(Type.Teleport)
                        
                        elif input_neighbor.x >= len(input[input_neighbor.y]) or input[input_neighbor.y][input_neighbor.x] == " ":
                            grid[neighbor].set_type(Type.Teleport)
        
        grid.update_cache()
        return grid

    def to_string(self, character_pos: Point, show_teleports: bool = False, distance_wall_dir: Direction = None, distance_teleport_dir: Direction = None, current_zone: bool = False) -> str:
        res = ""
        height_range = list(range(self.height) if show_teleports else range(1, self.height-1))
        width_range = list(range(self.width) if show_teleports else range(1, self.width-1))
        for j in height_range:
            for i in width_range:
                pos = Point(i, j)
                if pos == character_pos:
                    res += "C"
                    continue

                tile = self[pos]
                if tile.type == Type.Void:
                    res += " "
                elif tile.type == Type.Teleport:
                    res += ("@" if show_teleports else " ")
                elif tile.type == Type.Wall:
                    res += ("#" if not current_zone else str(tile.get_current_zone(self)))
                else:
                    if current_zone:
                        res += str(tile.get_current_zone(self))
                    else:
                        char = "."
                        if distance_wall_dir:
                            char = "." if tile.distance_to_wall[distance_wall_dir.value] is None else str(min(9, tile.distance_to_wall[distance_wall_dir.value]))
                        elif distance_teleport_dir:
                            char = "." if tile.distance_to_teleport[distance_teleport_dir.value] is None else str(min(9, tile.distance_to_teleport[distance_teleport_dir.value]))
                        res += char
            res += "\n"
        return res

    def __repr__(self) -> str:
        return self.to_string()

    def navigate(self, origin: Point, dir: Direction, dist: int) -> Point:
        curr_tile = self[origin]
        incr = get_incr(dir)
        # If there is a wall, move towards it
        if curr_tile.distance_to_wall[dir.value] is not None:
            return origin + (incr * min(dist, curr_tile.distance_to_wall[dir.value] - 1))

        # If there is no wall, there is a teleport
        # If we don't reach it, just move towards it and exit
        dist_teleport = curr_tile.distance_to_teleport[dir.value]
        if dist_teleport > dist:
            return origin + incr * dist

        # Otherwise, teleport and do it again with new dist
        teleport_pos = origin + incr * dist_teleport
        teleport_tile = self[teleport_pos]
        new_pos = teleport_tile.teleport_coordinates[dir.value]
        return self.navigate(new_pos, dir, dist - dist_teleport)

def solve(entries: List[str], zones, zone_mapping):
    input_grid = entries[:-2]
    instructions = entries[-1]

    pattern = "([RL]?)([0-9]+)"
    all_insts = re.findall(pattern, instructions)

    grid = Grid.from_input(input_grid, zones, zone_mapping)
    print(grid.to_string(Point(0,0), current_zone=True))

    for i in range(2):
        curr_pos = grid.topleft_pos
        curr_dir = Direction.Right

        for dir, dist in all_insts:
            if dir == "R":
                curr_dir = Direction((curr_dir.value + 1) % 4)
            elif dir == "L":
                curr_dir = Direction((curr_dir.value - 1) % 4)

            curr_pos = grid.navigate(curr_pos, curr_dir, int(dist))
        
        password = curr_pos.y * 1000 + curr_pos.x * 4 + (curr_dir.value + 2) % 4
        print(f"Part {i+1}: Password = {password}")

        if i == 0:
            grid.clear_teleport_cache()
            grid.update_cache(folded=False)

example_zones = {
    (2, 0): 1,
    (0, 1): 2,
    (1, 1): 3,
    (2, 1): 4,
    (2, 2): 5,
    (3, 2): 6
}

entry_zones = {
    (1, 0): 1,
    (2, 0): 2,
    (1, 1): 3,
    (1, 2): 4,
    (0, 2): 5,
    (0, 3): 6
}

example_mapping = [
    # 1 -> 3, 2, 6, 4
    [(lambda pos: Point(4 + pos.y, 4), Direction.Down),
    (lambda pos: Point(12 - pos.x, 4), Direction.Down),
    (lambda pos: Point(16, pos.y + 8), Direction.Left),
    None
    ],
    # 2 -> 6, 1, 3, 5
    [],
    # 3 -> 2, 1, 4, 5
    [],
    # 4 -> 3, 1, 6, 5
    [],
    # 5 -> 3, 4, 6, 2
    [],
    # 6 -> 5, 4, 1, 2
    []
]

entry_mapping = []

if __name__ == "__main__":
    print("For example:")
    solve(example_entries, example_zones, example_mapping)

    print("For my entry:")
    solve(entries, entry_zones, entry_mapping)

