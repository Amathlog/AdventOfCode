import copy
from typing import List, Tuple, Dict, Optional, Set
from aoc.common.parse_entry import parse_all
from aoc.common.utils import profile
from aoc.common.point import Point

entries, example_entries = parse_all(__file__, "entry.txt", "example.txt")

@profile
def solve(entry: List[str], nb_connections:int) -> int:
    junction_boxes: List[Point] = []
    circuits: List[Set[Point]] = []
    mapping: Dict[Point, Set[Point]] = {}
    for e in entry:
        p = Point(*map(int, e.split(",")))
        junction_boxes.append(p)
        
        mapping[p] = {p}
        circuits.append(mapping[p])
    
    pairs: List[Tuple[Point, Point, float]] = []
    for i in range(len(junction_boxes)):
        left = junction_boxes[i]
        for j in range(i+1, len(junction_boxes)):
            right = junction_boxes[j]

            pairs.append((left, right, left.squared_distance(right)))

    pairs = sorted(pairs, key=lambda x: x[2])
    
    i = 0
    while True:
        # Part 1 Stop
        if i == nb_connections:
            while True:
                try:
                    circuits.remove(set())
                except ValueError:
                    break

            circuits.sort(key=lambda x: len(x), reverse=True)

            part_1 = len(circuits[0]) * len(circuits[1]) * len(circuits[2])

        # Part 2 Stop
        if len(mapping[left]) == len(junction_boxes):
            part_2 = left.x * right.x
            break
        
        left, right, _ = pairs[i]
        i += 1

        if right in mapping[left]:
            continue

        mapping[left].update(mapping[right])
        to_update = list(mapping[right])
        mapping[right].clear()
        for item in to_update:
            mapping[item] = mapping[left]


    return part_1, part_2


if __name__ == "__main__":
    print("Part 1 and 2 example:", solve(example_entries, 10))
    print("Part 1 and 2 entry:", solve(entries, 1000))