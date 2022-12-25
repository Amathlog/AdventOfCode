from pathlib import Path
import os
import copy
from typing import List, Tuple, Dict

entry_file = Path(os.path.abspath(__file__)).parent / "entry.txt"
example_file = Path(os.path.abspath(__file__)).parent / "example.txt"

def parse_entry(path: str) -> List[str]:
    with path.open("r") as f:
        entries = f.readlines()

    for i in range(len(entries)):
        if entries[i][-1] == '\n':
            entries[i] = entries[i][:-1]

    return entries

entries = parse_entry(entry_file)
example_entries = parse_entry(example_file)

def from_snafu(value: str) -> int:
    res = 0
    for c in value:
        res *= 5
        if c == "-":
            res -= 1
        elif c == "=":
            res -= 2
        else:
            res += int(c)

    return res

def to_snafu(value: int) -> str:
    res = ""
    while value != 0:
        c = value % 5
        if c == 3:
            res += "="
            value += 2
        elif c == 4:
            res += "-"
            value += 1
        else:
            res += str(c)
        value //= 5

    return res[::-1]

def solve(entries: List[str]):
    res = 0
    for e in entries:
        res += from_snafu(e)

    print("Part 1: Sum of all numbers in decimal:", res)    
    print("Part 1: Sum of all numbers in snafu:", to_snafu(res))    

if __name__ == "__main__":
    print("For example:")
    solve(example_entries)

    print("For my entries:")
    solve(entries)