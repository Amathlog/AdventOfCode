from pathlib import Path
import os
import copy
import re
from typing import Tuple, List

entry_file = Path(os.path.abspath(__file__)).parent / "entry.txt"
example_file = Path(os.path.abspath(__file__)).parent / "example.txt"

with entry_file.open("r") as f:
    entries = f.readlines()

for i in range(len(entries)):
    if entries[i][-1] == '\n':
        entries[i] = entries[i][:-1]

with example_file.open("r") as f:
    example_entries = f.readlines()

for i in range(len(example_entries)):
    if example_entries[i][-1] == '\n':
        example_entries[i] = example_entries[i][:-1]

class Position:
    def __init__(self, x: int, y: int):
        self.x = int(x)
        self.y = int(y)

    def __add__(self, other: "Position") -> "Position":
        return Position(self.x + other.x, self.y + other.y)

    def __sub__(self, other: "Position") -> "Position":
        return Position(self.x - other.x, self.y - other.y)

    def distance_man(self, other) -> int:
        return abs(self.x - other.x) + abs(self.y - other.y)

    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, other: "Position") -> bool:
        return self.x == other.x and self.y == other.y

    def __ne__(self, other: "Position") -> bool:
        return not (self == other)
    
    def __repr__(self) -> str:
        return str((self.x, self.y))

class Sensor:
    def __init__(self, pos: Position, beacon: Position):
        self.pos = pos
        self.closest_beacon = beacon
        self.distance_to_closest = self.pos.distance_man(self.closest_beacon)

    def __hash__(self):
        return self.pos.__hash__()

    def __eq__(self, other: "Sensor") -> bool:
        return self.pos == other.pos

    def __ne__(self, other: "Sensor") -> bool:
        return not (self == other)

    def __repr__(self) -> str:
        return str(self.pos)

class Range:
    def __init__(self, min: int, max: int):
        self.min = min
        self.max = max

    def is_valid(self) -> bool:
        return self.min <= self.max

    def get_intersection(self, other: "Range") -> Tuple[bool, "Range"]:
        res = Range(max([self.min, other.min]), min([self.max, other.max]))
        return res.is_valid(), res

    def merge(self, other: "Range") -> Tuple[bool, "Range"]:
        does_intersect, intersect = self.get_intersection(other)
        if not does_intersect and (intersect.min - intersect.max) > 1:
            return False, None
        
        return True, Range(min(self.min, other.min), max(self.max, other.max))

    def __repr__(self) -> str:
        return f"{self.min}-{self.max}"

    def __eq__(self, other: "Range") -> bool:
        return self.min == other.min and self.max == other.max
    
    def __len__(self):
        return self.max - self.min + 1

    @staticmethod
    def reduce(ranges: List["Range"]) -> List["Range"]:
        ranges = sorted(ranges, key=lambda x: x.min)
        i = 0
        res = []
        while i < len(ranges):
            curr = ranges[i]
            i += 1
            for j in range(i, len(ranges)):
                mergeable, merge = curr.merge(ranges[j])
                if mergeable:
                    curr = merge
                    i += 1
                    continue
                else:
                    break

            res.append(curr)

        return res


def get_ranges(sensors: set[Sensor], beacons: set[Position], line_to_search: int, min_limit: int = None, max_limit: int = None) -> List[Range]:
    sensors_to_check: set[Sensor] = set()
    ranges: List[Range] = []

    for s in sensors:
        min_dist = abs(s.pos.y - line_to_search)
        if min_dist <= s.distance_to_closest:
            sensors_to_check.add(s)

            diff = s.distance_to_closest - min_dist
            min_range = s.pos.x - diff
            max_range = s.pos.x + diff
            if min_limit is not None:
                min_range = max(min_range, min_limit)
            if max_limit is not None:
                max_range = min(max_range, max_limit)

            ranges.append(Range(min_range, max_range))

    return Range.reduce(ranges)

def search(sensors: set[Sensor], beacons: set[Position], line_to_search: int) -> int:
    reduce_ranges = get_ranges(sensors, beacons, line_to_search)
    nb_beacons_in_range = 0
    for b in beacons:
        if b.y != line_to_search:
            continue

        for r in reduce_ranges:
            if r.min <= b.x and r.max >= b.x:
                nb_beacons_in_range += 1
                break

    return sum([len(r) for r in reduce_ranges]) - nb_beacons_in_range

def solve(entries: List[str], line_to_search: int, max_y: int):
    sensors: set[Sensor] = set()
    beacons: set[Position] = set()

    pattern = "Sensor at x=([\-0-9]+), y=([\-0-9]+): closest beacon is at x=([\-0-9]+), y=([\-0-9]+)"

    for e in entries:
        m = re.match(pattern, e)
        beacon = Position(*m.group(3,4))
        beacons.add(beacon)
        sensors.add(Sensor(Position(*m.group(1,2)), beacon))

    print("Part 1:", search(sensors, beacons, line_to_search))

    for y in range(max_y):
        ranges = get_ranges(sensors, beacons, y, 0, max_y)
        if len(ranges) == 2:
            x = ranges[0].max + 1
            print(f"Part 2: x = {x}; y = {y} => frequency = {4000000 * x + y}")
            break

if __name__ == "__main__":
    print("For example file:")
    solve(example_entries, 10, 20)

    print("For entry file:")
    solve(entries, 2000000, 4000000)