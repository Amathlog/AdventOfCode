from pathlib import Path
import os
import copy
from typing import List, Tuple, Dict, Optional, Callable
from enum import Enum
import re
import sys

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


class Tile:
    def __init__(self, pos: Point, _type: Type, zone_size: int):
        self.set_type(_type)
        self.pos = pos
        # Follow "Direction" enum index order
        self.teleport_coordinates: List[Tuple[Point, Direction]] = [None] * 4
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
        self.distance_to_wall = [None] * 4
        if self.type == Type.Teleport:
            self.teleport_coordinates = [None] * 4

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
                self.teleport_coordinates[initial_dir.value] = (curr.pos - neighbor, initial_dir)

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
            curr_dir = get_opposite_direction(neighbor)
            next_zone, next_dir = grid.zone_mapping[curr_zone - 1][curr_dir.value]

            assert curr_zone != next_zone
            
            next_pos = grid.transform(curr.pos, curr_dir, curr_zone, next_dir, next_zone)
            next_tile = grid[next_pos]
            self.teleport_coordinates[curr_dir.value] = (next_tile.pos, get_opposite_direction(get_incr(next_dir)))
            if next_tile.type == Type.Wall:
                self.distance_to_wall[curr_dir.value] = 0
                
    def update_cache(self, grid: "Grid", second_time: bool = False, folded: bool = False):
        if self.visited and (not second_time or self.visited_twice):
            return

        self.visited = True
        if second_time:
            self.visited_twice = True

        if self.type == Type.Wall:
            self.distance_to_wall = [0] * 4
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
        self.zone_mapping: List[List[Tuple[int, Direction]]] = zone_mapping

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

    def validation(self):
        for j in range(self.height):
            for i in range(self.width):
                tile = self.grid[j][i]
                if tile.type == Type.Empty:
                    # Validate that all directions are valid
                    for dir in range(4):
                        assert tile.distance_to_wall[dir] is not None or tile.distance_to_teleport[dir] is not None
                        assert tile.distance_to_wall[dir] is None or tile.distance_to_wall[dir] >= 0
                        assert tile.distance_to_teleport[dir] is None or tile.distance_to_teleport[dir] >= 0
                
                elif tile.type == Type.Teleport:
                    for dir in range(len(tile.teleport_coordinates)):
                        if tile.teleport_coordinates[dir] is None:
                            continue

                        curr_dir = Direction(dir)
                        curr_pos = tile.pos + get_incr(curr_dir) * -1
                        curr_tile = self[curr_pos]
                        assert curr_tile.type == Type.Empty

                        new_pos, new_dir = tile.teleport_coordinates[dir]
                        new_tile = self[new_pos]
                        assert new_pos != curr_pos
                        opposite_new_dir = get_opposite_direction(get_incr(new_dir))
                        other_teleport = self[new_pos + get_incr(opposite_new_dir)]
                        assert other_teleport.type == Type.Teleport

                        if new_tile.type == Type.Wall:
                            assert other_teleport.teleport_coordinates[opposite_new_dir.value] is None
                            assert tile.distance_to_wall[dir] == 0
                        else:
                            other_pos, other_dir = other_teleport.teleport_coordinates[opposite_new_dir.value]
                            assert curr_pos == other_pos
                            assert abs(other_dir.value - curr_dir.value) == 2

    def update_cache(self, folded: bool = False):
        for j in range(self.height):
            for i in range(self.width):
                tile = self.grid[j][i]
                tile.update_cache(self, folded=folded)

        for j in reversed(range(self.height)):
            for i in reversed(range(self.width)):
                tile = self.grid[j][i]
                tile.update_cache(self, second_time=True, folded=folded)

        self.validation()

    def clear_teleport_cache(self):
        for j in range(self.height):
            for i in range(self.width):
                self.grid[j][i].clear_teleport_cache()

    def get_origin_and_vec_dir(self, zone: int, dir: Direction):
        for (column_id, row_id), tentative_zone in self.zones.items():
            if tentative_zone == zone:
                break

        origin = Point(column_id * self.zone_size, row_id * self.zone_size)
        if dir == Direction.Left:
            vec_dir = Point(0, 1)
        elif dir == Direction.Up:
            vec_dir = Point(1, 0)
        elif dir == Direction.Right:
            origin += Point(self.zone_size - 1, self.zone_size - 1)
            vec_dir = Point(0, -1)
        else:
            origin += Point(self.zone_size - 1, self.zone_size - 1)
            vec_dir = Point(-1, 0)

        return origin, vec_dir

    def transform(self, pos: "Point", initial_dir: Direction, initial_zone: int, new_dir: Direction, new_zone: int) -> "Point":
        transform_number = (initial_dir.value - new_dir.value) % 4
        translated_pos = Point(pos.x - 1, pos.y - 1)

        initial_origin, _ = self.get_origin_and_vec_dir(initial_zone, initial_dir)
        alpha = translated_pos.distance(initial_origin)
        new_origin, new_vec_dir = self.get_origin_and_vec_dir(new_zone, new_dir)

        if transform_number == 0 or transform_number == 2:
            alpha = self.zone_size - alpha - 1
       
        new_translated_pos = new_origin + new_vec_dir * alpha
        return Point(new_translated_pos.x + 1, new_translated_pos.y + 1)

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

    def to_string(self, character_pos: Point, show_teleports: bool = False, distance_wall_dir: Direction = None, distance_teleport_dir: Direction = None, current_zone: bool = False, visited_positions = None) -> str:
        res = ""
        height_range = list(range(self.height) if show_teleports else range(1, self.height-1))
        width_range = list(range(self.width) if show_teleports else range(1, self.width-1))

        for j in height_range:
            for i in width_range:
                pos = Point(i, j)
                if pos == character_pos:
                    res += "\x1b[1;37mC"
                    continue

                if visited_positions is not None and pos in visited_positions:
                    dir, id = visited_positions[pos]
                    color = id % 255
                    res += f"\x1b[38;5;{color}m"

                    if dir == Direction.Left:
                        res += "<"
                    elif dir == Direction.Right:
                        res += ">"
                    elif dir == Direction.Up:
                        res += "^"
                    else:
                        res += "v"
                    continue

                res += "\x1b[0;37m"

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

    def debug_teleport(self, zone: int) -> str:
        res = ""

        all_teleport_positions = {}
        id = 0

        for j in range(self.height):
            for i in range(self.width):
                pos = Point(i, j)
                tile = self[pos]
                if tile.type != Type.Empty:
                    continue

                if zone != tile.get_current_zone(self):
                    continue

                for dir in range(4):
                    if tile.distance_to_teleport[dir] != 0 and tile.distance_to_wall[dir] is None:
                        teleport_pos = pos + get_incr(Direction(dir)) * tile.distance_to_teleport[dir]
                        teleport_tile = self[teleport_pos]
                        assert teleport_tile.type == Type.Teleport
                        if teleport_pos in all_teleport_positions:
                            continue

                        all_teleport_positions[teleport_pos] = (Direction(dir), id)
                        new_pos, new_dir = teleport_tile.teleport_coordinates[dir]
                        all_teleport_positions[new_pos] = (new_dir, id)
                        id += 1
        
        return self.to_string(Point(0,0), show_teleports=True, visited_positions=all_teleport_positions)

    def __repr__(self) -> str:
        return self.to_string()

    def navigate(self, origin: Point, dir: Direction, dist: int, id: int) -> Tuple[Point, Direction]:
        curr_tile = self[origin]
        incr = get_incr(dir)
        # If there is a wall, move towards it
        if curr_tile.distance_to_wall[dir.value] is not None:
            dist = min(dist, curr_tile.distance_to_wall[dir.value] - 1)
            all_positions = {origin + incr * i: (dir, id) for i in range(dist)}
            return origin + incr * dist, dir, all_positions 

        # If there is no wall, there is a teleport
        # If we don't reach it, just move towards it and exit
        dist_teleport = curr_tile.distance_to_teleport[dir.value]
        if dist_teleport > dist:
            all_positions = {origin + incr * i: (dir, id) for i in range(dist)}
            return origin + incr * dist, dir, all_positions

        # Otherwise, teleport and do it again with new dist
        teleport_pos = origin + incr * dist_teleport
        teleport_tile = self[teleport_pos]
        assert teleport_tile.type == Type.Teleport
        new_pos, new_dir = teleport_tile.teleport_coordinates[dir.value]
        final_pos, final_dir, all_positions = self.navigate(new_pos, new_dir, dist - dist_teleport, id)
        all_positions.update({origin + incr * i: (dir, id) for i in range(dist_teleport)})
        return final_pos, final_dir, all_positions

def solve(entries: List[str], zones, zone_mapping):
    input_grid = entries[:-2]
    instructions = entries[-1]

    pattern = "([RL]?)([0-9]+)"
    all_insts = re.findall(pattern, instructions)

    grid = Grid.from_input(input_grid, zones, zone_mapping)
    #print(grid.to_string(Point(0,0), current_zone=True))


    for i in range(2):
        all_visited_positions = {}
        curr_pos = grid.topleft_pos
        curr_dir = Direction.Right

        id = 0
        for dir, dist in all_insts:
            if dir == "R":
                curr_dir = Direction((curr_dir.value + 1) % 4)
            elif dir == "L":
                curr_dir = Direction((curr_dir.value - 1) % 4)

            curr_pos, curr_dir, visited_positions = grid.navigate(curr_pos, curr_dir, int(dist), id)
            all_visited_positions.update(visited_positions)
            assert grid[curr_pos].type == Type.Empty
            id += 1

            #print(f"{dir}: {dist}")
        # print(grid.to_string(curr_pos, visited_positions=all_visited_positions))
        
        password = curr_pos.y * 1000 + curr_pos.x * 4 + (curr_dir.value + 2) % 4
        print(f"Part {i+1}: Password = {password}")

        if i == 0:
            grid.clear_teleport_cache()
            grid.update_cache(folded=True)
            # for i in range(1, 7):
            #     print(f"Teleport for zone {i}")
            #     print(grid.debug_teleport(i))

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
    [(3, Direction.Up),
    (2, Direction.Up),
    (6, Direction.Right),
    None],
    # 2 -> 6, 1, 3, 5
    [(6, Direction.Down),
    (1, Direction.Up),
    None,
    (5, Direction.Down)],
    # 3 -> 2, 1, 4, 5
    [None,
    (1, Direction.Left),
    None,
    (5, Direction.Left)],
    # 4 -> 3, 1, 6, 5
    [None,
    None,
    (6, Direction.Up),
    None],
    # 5 -> 3, 4, 6, 2
    [(3, Direction.Down),
    None,
    None,
    (2, Direction.Down)],
    # 6 -> 5, 4, 1, 2
    [None,
    (4, Direction.Right),
    (1, Direction.Right),
    (2, Direction.Left)]
]

entry_mapping = [
    # 1 -> 5, 6, 2, 3
    [
        (5, Direction.Left),
        (6, Direction.Left),
        None,
        None
    ],
    # 2 -> 1, 6, 4, 3
    [
        None,
        (6, Direction.Down),
        (4, Direction.Right),
        (3, Direction.Right),
    ],
    # 3 -> 5, 1, 2, 4
    [
        (5, Direction.Up),
        None,
        (2, Direction.Down),
        None
    ],
    # 4 -> 5, 3, 2, 6
    [
        None,
        None,
        (2, Direction.Right),
        (6, Direction.Right)
    ],
    # 5 -> 1, 3, 4, 6
    [
        (1, Direction.Left),
        (3, Direction.Left),
        None,
        None
    ],
    # 6 -> 1, 5, 4, 2
    [
        (1, Direction.Up),
        None,
        (4, Direction.Down),
        (2, Direction.Up)
    ]
]

if __name__ == "__main__":
    print("For example:")
    solve(example_entries, example_zones, example_mapping)

    print("For my entry:")
    solve(entries, entry_zones, entry_mapping)

