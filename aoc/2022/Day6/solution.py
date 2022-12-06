from pathlib import Path
import os
import copy

entry_file = Path(os.path.abspath(__file__)).parent / "entry.txt"
example_file = Path(os.path.abspath(__file__)).parent / "example.txt"

with entry_file.open("r") as f:
    entries = f.readlines()

for i in range(len(entries)):
    if entries[i][-1] == '\n':
        entries[i] = entries[i][:-1]

def detector(input: str, n: int = 4) -> int:
    for i in range(n, len(input)):
        cache = set(list(input[i-n:i]))
        if len(cache) == n:
            return i

    return -1

print("Part 1: Number of elements before 4 different letters =", detector(entries[0]))
print("Part 2: Number of elements before 14 different letters =", detector(entries[0], 14))
