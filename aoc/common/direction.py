from aoc.common.point import Point
from enum import IntEnum

class Direction(IntEnum):
    North = 0,
    NorthEast = 1,
    East = 2,
    SouthEast = 3,
    South = 4,
    SouthWest = 5,
    West = 6,
    NorthWest = 7

dir_to_incr = [
    Point(-1, 0),
    Point(-1, 1),
    Point(0, 1),
    Point(1, 1),
    Point(1, 0),
    Point(1, -1),
    Point(0, -1),
    Point(-1, -1)
]

def advance(pos: Point, dir: Direction, num: int = 1) -> Point:
    return pos + dir_to_incr[dir] * num

def advance_inplace(pos: Point, dir: Direction, num: int = 1) -> None:
    pos += dir_to_incr[dir] * num

def backtrack(pos: Point, dir: Direction, num: int = 1) -> Point:
    return pos + dir_to_incr[turn_clockwise(dir, 180)] * num

def backtrack_inplace(pos: Point, dir: Direction, num: int = 1) -> None:
    pos += dir_to_incr[turn_clockwise(dir, 180)] * num

def turn_clockwise(dir: Direction, angle: int) -> Direction:
    while angle < 0:
        angle = 360 + angle
    while angle >= 360:
        angle -= 360

    incr = angle // 45
    return Direction((int(dir) + incr) % 8)

def turn_counterclockwise(dir: Direction, angle: int) -> Direction:
    return turn_clockwise(dir, -angle)
