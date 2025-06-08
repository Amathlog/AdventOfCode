import copy
from typing import List, Tuple, Dict, Optional, Set
from aoc.common.parse_entry import parse_all_multiple_parts, default_separator
from aoc.common.utils import profile

entries, example_entries = parse_all_multiple_parts(__file__, default_separator, 3, "entry.txt", "example.txt")

def print_columns(columns: List[List[int]], top_only: bool = False):
    res = ""
    iter = max([len(c) for c in columns]) if not top_only else 1
    for j in range(iter):
        for c in columns:
            if j < len(c):
                res += str(c[j])
            else:
                res += " "
            res += " "
        if not top_only:
            res += "\n"
    return res

def parse_input(entry: List[str]) -> List[List[int]]:
    columns: List[List[int]] = []
    for e in entry:
        for j, c in enumerate(e.split()):
            if len(columns) <= j:
                columns.append([])
            columns[j].append(int(c))
    return columns

def step(columns: List[List[int]], i: int):
    curr_col = columns[i % 4]
    curr_dancer = curr_col.pop(0)
    next_col = columns[(i + 1) % 4]
    comp_index = curr_dancer % (len(next_col) * 2)
    if len(next_col) >= comp_index:
        next_col.insert(comp_index - 1, curr_dancer)
    else:
        next_col.insert(comp_index - len(next_col) + 1, curr_dancer)

@profile
def part_one(entry: List[str]) -> int:
    columns = parse_input(entry)
    nb_rounds = 10
    for i in range(nb_rounds):
        step(columns, i)

    return print_columns(columns, top_only=True)

@profile
def part_two(entry: List[str]) -> int:
    columns = parse_input(entry)
    nb_rounds = 0
    seen = {}
    while True:
        step(columns, nb_rounds)
        nb_rounds += 1
        shout = print_columns(columns, top_only=True)
        if shout not in seen:
            seen[shout] = 0
        seen[shout] += 1
        if seen[shout] == 2024:
            break
        
    shout = int(shout.replace(" ", ""))
    return shout * nb_rounds

@profile
def part_three(entry: List[str]) -> int:
    return 0


if __name__ == "__main__":
    print("Part 1 example:", part_one(example_entries[0]))
    print("Part 1 entry:", part_one(entries[0]))

    print("Part 2 example:", part_two(example_entries[1]))
    print("Part 2 entry:", part_two(entries[1]))

    print("Part 3 example:", part_three(example_entries[2]))
    print("Part 3 entry:", part_three(entries[2]))
