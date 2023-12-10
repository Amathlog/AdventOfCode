from pathlib import Path
import os
import copy
from typing import List, Tuple, Dict, Set
from aoc.common.parse_entry import parse_all
from enum import IntEnum, auto
from aoc.common.point import Point
from aoc.common.grid import Grid

entries, example_entries, example_entries2, example_entries3, example_entries4 = parse_all(__file__, "entry.txt", "example.txt", "example2.txt", "example3.txt", "example4.txt")

class Direction(IntEnum):
    Up = 0
    Right = 1
    Down = 2
    Left = 3

left_incr = Point(0, -1)
right_incr = Point(0, 1)
up_incr = Point(-1, 0)
down_incr = Point(1, 0)

def next(pos: Point, dir: Direction, sketch: Grid) -> Tuple[Point, Direction, bool]:
    if not sketch.is_valid(pos):
        return None, None, False
    
    tile = sketch[pos]
    new_dir = dir
    if tile == "|":
        if dir != Direction.Up and dir != Direction.Down:
            return None, None, False
    elif tile == "-":
        if dir != Direction.Left and dir != Direction.Right:
            return None, None, False
    elif tile == "L":
        if dir == Direction.Down:
            new_dir = Direction.Right
        elif dir == Direction.Left:
            new_dir = Direction.Up
        else:
            return None, None, False
    elif tile == "J":
        if dir == Direction.Right:
            new_dir = Direction.Up
        elif dir == Direction.Down:
            new_dir = Direction.Left
        else:
            return None, None, False
    elif tile == "7":
        if dir == Direction.Right:
            new_dir = Direction.Down
        elif dir == Direction.Up:
            new_dir = Direction.Left
        else:
            return None, None, False
    elif tile == "F":
        if dir == Direction.Up:
            new_dir = Direction.Right
        elif dir == Direction.Left:
            new_dir = Direction.Down
        else:
            return None, None, False
    else:
        return None, None, False

    if new_dir == Direction.Up:
        return pos + up_incr, new_dir, True
    if new_dir == Direction.Left:
        return pos + left_incr, new_dir, True
    if new_dir == Direction.Right:
        return pos + right_incr, new_dir, True
    
    return pos + down_incr, new_dir, True

def get_all_inside_points(pipe: List[Point], dirs: List[Direction], sketch: Grid, clockwise: bool, retried: bool = False):
    pipe_set = set(pipe)
    inside_pts = set()

    # For each point in pipe, dependending on the current direction (and clockwise) we increment our position until we reach
    # another pipe. All points found that way are inside.
    for i in range(len(pipe)):
        pos = pipe[i]
        dir = dirs[i]

        if dir == Direction.Up:
            incr = right_incr if clockwise else left_incr
        elif dir == Direction.Down:
            incr = left_incr if clockwise else right_incr
        elif dir == Direction.Left:
            incr = up_incr if clockwise else down_incr
        else:
            incr = down_incr if clockwise else up_incr

        pos += incr
        while pos not in pipe_set:
            if not sketch.is_valid(pos):
                if not retried:
                    # If we reached the limit of our grid, it means our clockwise assumption was false, so retry with clockwise = false
                    return get_all_inside_points(pipe, dirs, sketch, not clockwise, True)
                else:
                    return None
                
            if pos in inside_pts:
                break

            inside_pts.add(pos)
            pos += incr

    return inside_pts


def part_one_and_two(entry: List[str]) -> int:
    sketch = Grid(entry)
    start = Point()
    stop = False
    for i, e in enumerate(entry):
        for j, c in enumerate(e):
            if c == "S":
                start = Point(i, j)
                stop = True
                break
        if stop:
            break

    curr = None
    previous_dir = None
    for p, dir in [(start + up_incr, Direction.Up), (start + left_incr, Direction.Left), (start + right_incr, Direction.Right), (start + down_incr, Direction.Down)]:
        if next(p, dir, sketch)[2]:
            if curr is None:
                curr = (p, dir)
            else:
                # reversed
                previous_dir = Direction((int(dir) + 2) % 4)

    steps = 1
    pipe = [start]
    dirs = [previous_dir]
    corners = set(["7", "J", "F", "L"])
    while True:
        pipe.append(curr[0])
        dirs.append(curr[1])

        tile = sketch[curr[0]]

        steps += 1
        next_p, next_dir, success = next(curr[0], curr[1], sketch)
        assert(success)

        if next_p == start:
            break

        # If it is a corner, it has 2 directions, so duplicate the point with the new direction.
        if tile in corners:
            pipe.append(curr[0])
            dirs.append(next_dir)

        curr = (next_p, next_dir)

    inside_pts = get_all_inside_points(pipe, dirs, sketch, True)

    return steps // 2, len(inside_pts)


if __name__ == "__main__":
    print("Part 1 and 2 example:", part_one_and_two(example_entries))
    print("Part 1 and 2 example2:", part_one_and_two(example_entries2))
    print("Part 1 and 2 example3:", part_one_and_two(example_entries3))
    print("Part 1 and 2 example4:", part_one_and_two(example_entries4))
    print("Part 1 and 2 entry:", part_one_and_two(entries))
