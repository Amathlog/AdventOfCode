import copy
from typing import List, Tuple, Dict, Optional, Set
from aoc.common.parse_entry import parse_all
from aoc.common.utils import profile
from aoc.common.point import Point
import re
from functools import reduce

entries, example_entries = parse_all(__file__, "entry.txt", "example.txt")

def simulate(start: Point, vel: Point, limits: Point, steps: int):
    new_pos = start + vel * steps
    new_pos.x = new_pos.x % limits.x
    new_pos.y = new_pos.y % limits.y
    return new_pos

def get_all_robots(entry: List[str]):
    regex = re.compile("p=(-?\d+),(-?\d+) v=(-?\d+),(-?\d+)")
    robots = []
    for line in entry:
        p_x, p_y, v_x, v_y = regex.findall(line)[0]
        robots.append([Point(int(p_x), int(p_y)), Point(int(v_x), int(v_y))])

    return robots

def get_quadrant(pos: Point, middle: Point) -> int:
    quadrant = 0
    if pos.x > middle.x:
        quadrant = 2
    elif pos.x == middle.x:
        return None
    if pos.y > middle.y:
        quadrant += 1
    elif pos.y == middle.y:
        return None
    
    return quadrant

@profile
def part_one(entry: List[str]) -> int:
    limits = Point(101,103)
    middle = limits // 2
    nb_steps = 100
    quadrants = [0] * 4
    for pos, vel in get_all_robots(entry):
        new_pos = simulate(pos, vel, limits, nb_steps)
        quadrant = get_quadrant(new_pos, middle)
        if quadrant is not None:
            quadrants[quadrant] += 1

    return reduce(lambda x, y: x*y, quadrants)


@profile
def part_two(entry: List[str]) -> int:
    robots = get_all_robots(entry)
    limits = Point(101,103)
    middle = limits // 2
    def print_robots():
        sorted_robots = sorted(robots, key=lambda r: r[0].x * limits.y + r[0].y)
        curr = 0
        res = ""
        for i in range(limits.x):
            for j in range(limits.y):
                nb_robots = 0
                while curr < len(sorted_robots) and sorted_robots[curr][0].x == i and sorted_robots[curr][0].y == j:
                    nb_robots += 1
                    curr += 1
                if nb_robots >= 10:
                    res += "X"
                elif nb_robots == 0:
                    res += "."
                else:
                    res += str(nb_robots)
            res += "\n"
        assert curr == len(sorted_robots)
        print(res)

    min_quadrants = 999999999999999999999999999999999
    min_index = -1
    for iter in range(10000):
        quadrants = [0] * 4
        for i in range(len(robots)):
            robots[i][0] = simulate(robots[i][0], robots[i][1], limits, 1)
            quadrant = get_quadrant(robots[i][0], middle)
            if quadrant is not None:
                quadrants[quadrant] += 1
        
        quadrant_value = reduce(lambda x, y: x*y, quadrants)
        if quadrant_value < min_quadrants:
            min_index = iter
            min_quadrants = quadrant_value

    return(min_index + 1)


if __name__ == "__main__":
    print("Part 1 example:", part_one(example_entries))
    print("Part 1 entry:", part_one(entries))

    print("Part 2 example:", part_two(example_entries))
    print("Part 2 entry:", part_two(entries))
