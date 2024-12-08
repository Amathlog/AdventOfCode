from typing import List, Dict, Callable
from aoc.common.parse_entry import parse_all
from aoc.common.utils import profile
from aoc.common.grid import Point, Grid


entries, example_entries = parse_all(__file__, "entry.txt", "example.txt")


def get_antipods(a: Point, b: Point, grid: Grid) -> List[Point]:
    dir = (b - a)
    result = []
    antipod_1 = a - dir
    antipod_2 = b + dir
    if grid.is_valid(antipod_1): result.append(antipod_1)
    if grid.is_valid(antipod_2): result.append(antipod_2)
    return result


def get_all_antipods(a: Point, b: Point, grid: Grid) -> List[Point]:
    dir = (b - a)
    result = []
    for start, real_dir in zip((a,b), (dir, dir * -1)):
        curr = start + real_dir
        while grid.is_valid(curr):
            result.append(curr)
            curr = curr + real_dir

    return result


def get_mapping(entry: List[str]) -> Dict[str, List[Point]]:
    mapping = {}

    for i, line in enumerate(entry):
        for j, c in enumerate(line):
            if c == ".":
                continue
            if c not in mapping:
                mapping[c] = []
            mapping[c].append(Point(i,j))

    return mapping


def for_each_pair(entry: List[str], callback: Callable[[Point, Point, Grid], List[Point]]) -> int:
    mapping = get_mapping(entry)
    grid = Grid(entry)
    unique_antipods = set()

    for pos in mapping.values():
        for i in range(len(pos)):
            a = pos[i]
            for j in range(i+1, len(pos)):
                b = pos[j]
                unique_antipods.update(callback(a, b, grid))

    return len(unique_antipods)


@profile
def part_one(entry: List[str]) -> int:
    return for_each_pair(entry, get_antipods)


@profile
def part_two(entry: List[str]) -> int:
    return for_each_pair(entry, get_all_antipods)


if __name__ == "__main__":
    print("Part 1 example:", part_one(example_entries))
    print("Part 1 entry:", part_one(entries))

    print("Part 2 example:", part_two(example_entries))
    print("Part 2 entry:", part_two(entries))
