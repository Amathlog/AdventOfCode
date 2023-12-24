import copy
from typing import List, Tuple, Dict, Optional, Set
from aoc.common.parse_entry import parse_all
from aoc.common.utils import profile
from aoc.common.direction import *
from aoc.common.grid import Grid
from aoc.common.point import Point

entries, example_entries = parse_all(__file__, "entry.txt", "example.txt")

class Segment:
    def __init__(self, start: Point, dir: Direction, length: int, color: str):
        self.start = start
        self.dir = dir
        self.length = length
        self.color = color

    def get_all_points(self):
        return [advance(self.start, self.dir, i) for i in range(1, self.length + 1)]

def get_all_inside_points(segments: List[Segment], points: List[Point], min_point: Point, max_point: Point, clockwise: bool, retried: bool = False):
    all_points = set(points)
    inside_pts = set()

    # For each point in segment, dependending on the current direction (and clockwise) we increment our position until we reach
    # another segement. All points found that way are inside.
    for segment in segments:
        curr = segment.start
        incr = dir_to_incr[turn_clockwise(segment.dir, 90)] if clockwise else dir_to_incr[turn_counterclockwise(segment.dir, 90)]
        for _ in range(segment.length + 1):
            pos = curr + incr
            while pos not in all_points:
                if pos.x > max_point.x or pos.y > max_point.y or pos.x < min_point.x or pos.y < min_point.y:
                    if not retried:
                        # If we reached the limit of our grid, it means our clockwise assumption was false, so retry with clockwise = false
                        return get_all_inside_points(segments, points, min_point, max_point, not clockwise, True)
                    else:
                        return None
                    
                inside_pts.add(pos)
                pos += incr
            curr = advance(curr, segment.dir)
        
    return inside_pts

def compute_digs(entry: List[str]):
    segments = []
    points = []

    curr = Point(0, 0)
    for e in entry:
        dir, num, color = e.split()
        if dir == "U":
            dir = Direction.North
        elif dir == "L":
            dir = Direction.West
        elif dir == "D":
            dir = Direction.South
        else:
            dir = Direction.East

        num = int(num)
        segments.append(Segment(curr, dir, num, color[1:-1]))
        points.extend(segments[-1].get_all_points())
        curr = points[-1]

    min_point = Point(0, 0)
    max_point = Point(0, 0)

    min_point.x = min(points, key=lambda p: p.x).x
    min_point.y = min(points, key=lambda p: p.y).y
    max_point.x = max(points, key=lambda p: p.x).x
    max_point.y = max(points, key=lambda p: p.y).y

    return segments, points, min_point, max_point


@profile
def part_one(entry: List[str]) -> int:
    segments, points, min_point, max_point = compute_digs(entry)
    return len(points) + len(get_all_inside_points(segments, points, min_point, max_point, True))

@profile
def part_two(entry: List[str]) -> int:
    return 0


if __name__ == "__main__":
    print("Part 1 example:", part_one(example_entries))
    print("Part 1 entry:", part_one(entries))

    print("Part 2 example:", part_two(example_entries))
    print("Part 2 entry:", part_two(entries))
