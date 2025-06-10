import copy
from typing import List, Tuple, Dict, Optional, Set, Callable
from aoc.common.parse_entry import parse_all
from aoc.common.utils import profile
from collections import namedtuple

entries, example_entries = parse_all(__file__, "entry.txt", "example.txt")

def add_point(p1: Tuple, p2: Tuple):
    return tuple(p1[i] + p2[i] for i in range(len(p1)))


def generate_neighbors(p: Tuple, discard_p: bool):
    num_neighbors = 3 ** len(p)
    for i in range(num_neighbors):
        offset = [0] * len(p)
        for j in range(len(p)):
            div = 3 ** j
            idx = (i // div) % 3
            offset[j] = [-1, 0, 1][idx]

        if discard_p and not any(offset):
            continue

        yield add_point(p, offset)

def cycle(actives: Set[Tuple]) -> Set[Tuple]:
    # For each active point, we'll evaluate -1,-1,-1 and 1, 1, 1 cubes
    cubes_to_evaluate: Set[Tuple] = set()
    for c in actives:
        for other in generate_neighbors(c, False):
            cubes_to_evaluate.add(other)
    
    new_actives: Set[Tuple] = set()
    for c in cubes_to_evaluate:
        count = 0
        for other in generate_neighbors(c, True):
            if other in actives:
                count += 1
            
            if count > 3:
                break
        
        if c in actives:
            if 2 <= count <= 3:
                new_actives.add(c)
        else:
            if count == 3:
                new_actives.add(c)
    
    return new_actives

@profile
def part_one(entry: List[str]) -> int:
    actives: Set[Tuple] = set()
    z = 0
    for x, line in enumerate(entry):
        for y, c in enumerate(line):
            if c == "#":
                p = (x, y, z)
                actives.add(p)
    for i in range(6):
        actives = cycle(actives)

    return len(actives)

@profile
def part_two(entry: List[str]) -> int:
    actives: Set[Tuple] = set()
    z = 0
    w = 0
    for x, line in enumerate(entry):
        for y, c in enumerate(line):
            if c == "#":
                p = (x, y, z, w)
                actives.add(p)
    for i in range(6):
        actives = cycle(actives)

    return len(actives)


if __name__ == "__main__":
    print("Part 1 example:", part_one(example_entries))
    print("Part 1 entry:", part_one(entries))

    print("Part 2 example:", part_two(example_entries))
    print("Part 2 entry:", part_two(entries))
