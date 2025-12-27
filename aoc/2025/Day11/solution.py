import copy
from typing import List, Tuple, Dict, Optional, Set
from aoc.common.parse_entry import parse_all
from aoc.common.utils import profile

entries, example_entries, example_entries2 = parse_all(__file__, "entry.txt", "example.txt", "example2.txt")

def recurse(start: str, end: str, transitions: Dict[str, List[str]], known: Dict[str, int]):
    if start == end:
        return 1
    
    if start in known:
        return known[start]
    
    next = transitions[start]
    res = 0
    for n in next:
        res += recurse(n, end, transitions, known)
    
    known[start] = res
    return res


@profile
def part_one(entry: List[str]) -> int:
    transitions: Dict[str, List[str]] = {}

    for e in entry:
        device, next = e.split(": ")
        transitions[device] = next.split(" ")

    return recurse("you", "out", transitions, {})


@profile
def part_two(entry: List[str]) -> int:
    transitions: Dict[str, List[str]] = {}

    for e in entry:
        device, next = e.split(": ")
        transitions[device] = next.split(" ")

    transitions["out"] = []

    nb_paths_from_svr_to_fft = recurse("svr", "fft", transitions, {})
    nb_paths_from_fft_to_dac = recurse("fft", "dac", transitions, {})
    nb_paths_from_dac_to_out = recurse("dac", "out", transitions, {})

    nb_paths_from_svr_to_dac = recurse("svr", "dac", transitions, {})
    nb_paths_from_dac_to_fft = recurse("dac", "fft", transitions, {})
    nb_paths_from_fft_to_out = recurse("fft", "out", transitions, {})

    return nb_paths_from_svr_to_fft * nb_paths_from_fft_to_dac * nb_paths_from_dac_to_out + \
        nb_paths_from_svr_to_dac * nb_paths_from_dac_to_fft * nb_paths_from_fft_to_out


if __name__ == "__main__":
    print("Part 1 example:", part_one(example_entries))
    print("Part 1 entry:", part_one(entries))

    print("Part 2 example:", part_two(example_entries2))
    print("Part 2 entry:", part_two(entries))
