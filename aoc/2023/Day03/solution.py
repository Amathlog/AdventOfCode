from pathlib import Path
import os
import copy
from typing import List, Tuple, Dict
from aoc.common.parse_entry import parse_all

entries, example_entries = parse_all(__file__, "entry.txt", "example.txt")

def is_digit(c: str) -> bool:
    return ord("0") <= ord(c) <= ord("9")

def get_all_symbols(i, start, end, entry):
    res = {}
    for row in [i-1, i, i+1]:
        if row < 0 or row >= len(entry):
            continue

        the_range = range(start-1, end+1) if row != i else [start-1, end]

        for col in the_range:
            if col < 0 or col >= len(entry[i]):
                continue
            c = entry[row][col]
            if is_digit(c) or c == ".":
                continue

            if c not in res:
                res[c] = []
            res[c].append((row, col))

    return res

def part_one_and_two(entry: List[str]) -> int:
    res = 0
    gear_numbers = {}
    for i in range(len(entry)):
        curr_num = 0
        start = 0
        for j in range(len(entry[i])):
            c = entry[i][j]
            if is_digit(c):
                if curr_num == 0:
                    start = j
                
                curr_num = curr_num * 10 + int(c)
                continue

            if curr_num != 0:
                all_symbols = get_all_symbols(i, start, j, entry)
                if len(all_symbols) != 0:
                    res += curr_num
                
                if "*" in all_symbols:
                    for coord in all_symbols["*"]:
                        if coord not in gear_numbers:
                            gear_numbers[coord] = []
                        gear_numbers[coord].append(curr_num)
                
                curr_num = 0
        
        if curr_num != 0:
            all_symbols = get_all_symbols(i, start, len(entry[i]), entry)
            if len(all_symbols) != 0:
                res += curr_num
            
            if "*" in all_symbols:
                for coord in all_symbols["*"]:
                    if coord not in gear_numbers:
                        gear_numbers[coord] = []
                    gear_numbers[coord].append(curr_num)
            
            curr_num = 0

    second_res = 0
    for numbers in gear_numbers.values():
        if len(numbers) == 2:
            second_res += numbers[0] * numbers[1]
    
    return res, second_res

if __name__ == "__main__":
    print("Part 1 and 2 example:", part_one_and_two(example_entries))
    print("Part 1 and 2 entry:", part_one_and_two(entries))
