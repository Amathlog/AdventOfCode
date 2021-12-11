from pathlib import Path
import os
from enum import IntEnum
from typing import Tuple

entry_file = Path(os.path.abspath(__file__)).parent / "entry.txt"

with entry_file.open("r") as f:
    entries = f.readlines()

for i in range(len(entries)):
    if entries[i][-1] == '\n':
        entries[i] = entries[i][:-1]

class Point:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def __mul__(self, alpha):
        return Point(self.x * alpha, self.y * alpha)

    def __rmul__(self, alpha):
        return self.__mul__(alpha)

    def l1_norm(self):
        return abs(self.x) + abs(self.y)

class Direction(IntEnum):
    EAST = 0
    NORTH = 1
    WEST = 2
    SOUTH = 3

def get_new_direction(old_dir: Direction, angle: int) -> Direction:
    angle %= 360
    nb_quarter_turns = angle // 90

    return Direction(((old_dir + nb_quarter_turns) % 4))

def rotate(old_pos: Point, angle: int) -> Point:
    angle %= 360
    nb_quarter_turns = angle // 90

    for _ in range(nb_quarter_turns):
        old_pos = Point(-old_pos.y, old_pos.x)

    return old_pos

def get_new_position(dir: Direction, old_pos: Point, magnitude: int) -> Point:
    displacement = None
    if dir == Direction.EAST:
        displacement = Point(1, 0)
    elif dir == Direction.NORTH:
        displacement = Point(0, 1)
    elif dir == Direction.WEST:
        displacement = Point(-1, 0)
    else:
        displacement = Point(0, -1)

    displacement *= magnitude

    return old_pos + displacement

def update_position_first_answer(curr_dir: Direction, curr_pos: Point, cmd: str) -> Tuple[Direction, Point]:
    value = int(cmd[1:])
    cmd = cmd[0]

    if cmd == "L":
        curr_dir = get_new_direction(curr_dir, value)
    elif cmd == "R":
        curr_dir = get_new_direction(curr_dir, -value)
    elif cmd == "F":
        curr_pos = get_new_position(curr_dir, curr_pos, value)
    elif cmd == "N":
        curr_pos = get_new_position(Direction.NORTH, curr_pos, value)
    elif cmd == "S":
        curr_pos = get_new_position(Direction.SOUTH, curr_pos, value)
    elif cmd == "W":
        curr_pos = get_new_position(Direction.WEST, curr_pos, value)
    elif cmd == "E":
        curr_pos = get_new_position(Direction.EAST, curr_pos, value)

    return curr_dir, curr_pos

def update_position_second_answer(ship_pos: Point, waypoint: Point, cmd: str) -> Tuple[Point, Point]:
    value = int(cmd[1:])
    cmd = cmd[0]

    if cmd == "L":
        waypoint = rotate(waypoint, value)
    elif cmd == "R":
        waypoint = rotate(waypoint, -value)
    elif cmd == "F":
        ship_pos = ship_pos + waypoint * value
    elif cmd == "N":
        waypoint = get_new_position(Direction.NORTH, waypoint, value)
    elif cmd == "S":
        waypoint = get_new_position(Direction.SOUTH, waypoint, value)
    elif cmd == "W":
        waypoint = get_new_position(Direction.WEST, waypoint, value)
    elif cmd == "E":
        waypoint = get_new_position(Direction.EAST, waypoint, value)

    return ship_pos, waypoint



if __name__ == "__main__":
    curr_dir = Direction.EAST
    curr_pos = Point(0, 0)

    for e in entries:
        curr_dir, curr_pos = update_position_first_answer(curr_dir, curr_pos, e)

    print("First answer:", curr_pos.l1_norm())

    ship_pos = Point(0, 0)
    waypoint = Point(10, 1)

    for e in entries:
        ship_pos, waypoint = update_position_second_answer(ship_pos, waypoint, e)

    print("Second answer:", ship_pos.l1_norm())
