from pathlib import Path
from typing import List, Tuple, Dict
from aoc.common.parse_entry import parse_all
from aoc.common.utils import profile
from multiprocessing import Pool

entries, example_entries = parse_all(__file__, "entry.txt", "example.txt")

class State:
    def __init__(self, e: str, damage_list: List[int], damage_count: int):
        self.e = e
        self.damage_list = tuple(damage_list)
        self.damage_count = damage_count

    def __eq__(self, other: "State") -> bool:
        return self.e == other.e and self.damage_list == other.damage_list and self.damage_count == other.damage_count 

    def __hash__(self) -> int:
        return hash((self.e, self.damage_list, self.damage_count))

def backtrack(e: str, damage_list: List[int], damage_count: int, cache: Dict[State, int]) -> int:
    if cache is None:
        cache: Dict[State, int] = {}

    if len(e) == 0:
        if len(damage_list) == 0:
            return 1
        elif len(damage_list) > 1:
            return 0
        elif damage_list[0] == damage_count:
            return 1
        else:
            return 0
        
    state = State(e, damage_list, damage_count)
    
    if state in cache:
        return cache[state]
    
    c = e[0]
    if c == "#":
        damage_count += 1
        if len(damage_list) == 0 or damage_count > damage_list[0]:
            cache[state] = 0
            return 0 # invalid
        
        res = backtrack(e[1:], damage_list, damage_count, cache)
        cache[state] = res
        return res
    elif c == ".":
        if len(damage_list) > 0:
            if damage_count != 0 and damage_count != damage_list[0]:
                cache[state] = 0
                return 0
            elif damage_count != 0:
                damage_list = damage_list[1:]

        res = backtrack(e[1:], damage_list, 0, cache)
        cache[state] = res
        return res
    elif c == "?":
        res = backtrack("#" + e[1:], damage_list, damage_count, cache) + backtrack("." + e[1:], damage_list, damage_count, cache)
        cache[state] = res
        return res
    else:
        assert(False)

@profile
def part_one(entry: List[str]) -> int:
    res = 0
    for e in entry:
        e, damage_list = e.split()
        damage_list = [int(d) for d in damage_list.split(",")]
        res += backtrack(e, damage_list, 0, None)
    return res

def expand_and_backtrack(e: str) -> int:
    e, damage_list = e.split()
    damage_list = [int(d) for d in damage_list.split(",")]
    e = "?".join([e] * 5)
    damage_list = damage_list * 5
    return backtrack(e, damage_list, 0, None)


@profile
def part_two(entry: List[str]) -> int:
    with Pool(16) as p:
        return sum(p.map(expand_and_backtrack, entry))


if __name__ == "__main__":
    print("Part 1 example:", part_one(example_entries))
    print("Part 1 entry:", part_one(entries))

    print("Part 2 example:", part_two(example_entries))
    print("Part 2 entry:", part_two(entries))

