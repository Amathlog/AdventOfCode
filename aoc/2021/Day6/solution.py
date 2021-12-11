from pathlib import Path
import os
from typing import List

entry_file = Path(os.path.abspath(__file__)).parent / "entry.txt"

with entry_file.open("r") as f:
    entries = f.readlines()

for i in range(len(entries)):
    if entries[i][-1] == '\n':
        entries[i] = entries[i][:-1]

ages_ = [int(x) for x in entries[0].split(",")]

def compute_ages(t: int, ages: List[int]) -> int:
    all_ages = [0 for _ in range(9)]
    for x in ages:
        all_ages[x] += 1

    for _ in range(t):
        new_all_ages = [0 for _ in range(9)]
        for i in range(1, 9):
            new_all_ages[i-1] = all_ages[i]

        new_all_ages[6] += all_ages[0]
        new_all_ages[8] = all_ages[0]
        all_ages = new_all_ages
        
    return sum(all_ages)

print("First answer:", compute_ages(80, ages_))
print("Second answer:", compute_ages(256, ages_))
