import copy
from typing import List, Tuple, Dict, Optional, Set
from aoc.common.parse_entry import parse_all
from aoc.common.utils import profile

entries, example_entries = parse_all(__file__, "entry.txt", "example.txt")

potions = {'A': 0, 'B': 1, 'C': 3, 'D': 5, 'x': 0}

def is_enemy(c: str) -> bool:
    return c != 'x'

def vague(entry: str, nb_enemies_max: int) -> int:
    count = 0
    for i in range(len(entry) // nb_enemies_max):
        nb_enemies = 0
        for j in range(nb_enemies_max):
            enemy = entry[i * nb_enemies_max + j]
            nb_enemies += int(is_enemy(enemy))
            count += potions[enemy]
        
        if nb_enemies == 2:
            count += 2
        elif nb_enemies == 3:
            count += 6

    return count

@profile
def part_one(entry: List[str]) -> int:
    return vague(entry[0], 1)

@profile
def part_two(entry: List[str]) -> int:
    return vague(entry[1], 2)

@profile
def part_three(entry: List[str]) -> int:
    return vague(entry[2], 3)


if __name__ == "__main__":
    print("Part 1 example:", part_one(example_entries))
    print("Part 1 entry:", part_one(entries))

    print("Part 2 example:", part_two(example_entries))
    print("Part 2 entry:", part_two(entries))

    print("Part 3 example:", part_three(example_entries))
    print("Part 3 entry:", part_three(entries))