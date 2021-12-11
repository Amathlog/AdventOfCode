from pathlib import Path
import os
import numpy as np

entry_file = Path(os.path.abspath(__file__)).parent / "entry.txt"

with entry_file.open("r") as f:
    entries = f.readlines()

for i in range(len(entries)):
    if entries[i][-1] == '\n':
        entries[i] = entries[i][:-1]

entries = [int(e) for e in entries[0].split(",")]
temp = [16,1,2,0,4,2,7,1,2,14]

def compute_fuel_first_answer(l):
    median = int(np.median(l))
    return sum([abs(e - median) for e in l])

print("First answer:", compute_fuel_first_answer(entries))

def compute_fuel_second_answer(l):
    mean = np.mean(l)
    floor = int(np.floor(mean))
    ceil = int(np.ceil(mean))
    res_1 = 0
    res_2 = 0
    for e in l:
        n1 = abs(e - floor)
        n2 = abs(e - ceil)
        res_1 += n1 * (n1+1) // 2
        res_2 += n2 * (n2+1) // 2
    return min(res_1, res_2)

print("Second answer:", compute_fuel_second_answer(entries))