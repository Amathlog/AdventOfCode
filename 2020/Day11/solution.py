from pathlib import Path
import os
from typing import List, Tuple
import itertools
import copy

entry_file = Path(os.path.abspath(__file__)).parent / "entry.txt"

with entry_file.open("r") as f:
    entries = f.readlines()

for i in range(len(entries)):
    if entries[i][-1] == '\n':
        entries[i] = entries[i][:-1]
    entries[i] = [c for c in entries[i]]

def count_occupied_seats_simple(grid: List[str], i: int, j: int):
    occupied = 0
    for i_, j_ in itertools.product((i-1, i, i+1), (j-1, j, j+1)):
        if i_ == i and j_ == j:
            continue
    
        if i_ < 0 or i_ >= len(grid):
            continue

        if j_ < 0 or j_ >= len(grid[i]):
            continue

        if grid[i_][j_] == "#":
            occupied += 1

    return occupied

def count_occupied_seats_complex(grid: List[str], i: int, j: int):
    occupied = 0
    for incr_i, incr_j in itertools.product((-1, 0, 1), (-1, 0, 1)):
        if incr_i == 0 and incr_j == 0:
            continue

        i_ = i
        j_ = j
        while True:
            i_ += incr_i
            j_ += incr_j
            if i_ < 0 or i_ >= len(grid):
                break

            if j_ < 0 or j_ >= len(grid[i]):
                break

            if grid[i_][j_] == "#":
                occupied += 1
                break
                
            if grid[i_][j_] == "L":
                break

    return occupied


def apply_rules(grid: List[str], max_count: int, simple_rules: bool) -> Tuple[List[str], int]:
    res = copy.deepcopy(grid)
    new_occupied_seats_count = 0
    for i, s in enumerate(grid):
        for j, c in enumerate(s):
            if c == '.':
                continue

            # Compute adjacents:
            if simple_rules:
                occupied = count_occupied_seats_simple(grid, i, j)
            else:
                occupied = count_occupied_seats_complex(grid, i, j)

            if c == "L" and occupied == 0:
                res[i][j] = "#"
            elif c == "#" and occupied >= max_count:
                res[i][j] = "L"

            if res[i][j] == "#":
                new_occupied_seats_count += 1
    
    return res, new_occupied_seats_count

def print_grid(grid):
    print("\n".join(["".join(x) for x in grid]))

grid = copy.deepcopy(entries)
max_count_first_answer = 4
new_grid, new_count = apply_rules(grid, max_count_first_answer, True)
while new_grid != grid:
    # print_grid(new_grid)
    # print()
    grid = copy.deepcopy(new_grid)
    new_grid, new_count = apply_rules(grid, max_count_first_answer, True)
    

print("First answer:", new_count)

grid = copy.deepcopy(entries)
max_count_second_answer = 5
new_grid, new_count = apply_rules(grid, max_count_second_answer, False)
while new_grid != grid:
    # print_grid(new_grid)
    # print()
    grid = copy.deepcopy(new_grid)
    new_grid, new_count = apply_rules(grid, max_count_second_answer, False)
    

print("Second answer:", new_count)