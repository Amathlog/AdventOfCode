from pathlib import Path
import os
import copy
from typing import List

entry_file = Path(os.path.abspath(__file__)).parent / "entry.txt"

with entry_file.open("r") as f:
    entries = f.readlines()

for i in range(len(entries)):
    if entries[i][-1] == '\n':
        entries[i] = entries[i][:-1]

def count_most_common(l: List, idx: int) -> int:
    count_0 = 0
    count_1 = 0

    for i in l:
        if i[idx] == "0":
            count_0 += 1
        else:
            count_1 += 1

    return 0 if count_0 > count_1 else 1

gamma = 0
epsilon = 0

for i in range(len(entries[0])):
    gamma <<= 1
    epsilon <<= 1
    if count_most_common(entries, i) == 1:
        gamma += 1
    else:
        epsilon += 1

print("Gamma:", gamma)
print("Epsilon:", epsilon)
print("First answer:", gamma*epsilon)

split_o2 = copy.deepcopy(entries)
split_co2 = copy.deepcopy(entries)

for i in range(len(entries[0])):
    if len(split_o2) > 1:
        most_common = count_most_common(split_o2, i)

        split_o2 = [x for x in split_o2 if int(x[i]) == most_common]

    if len(split_co2) > 1:
        most_common = count_most_common(split_co2, i)

        split_co2 = [x for x in split_co2 if int(x[i]) != most_common]

o2 = int(split_o2[0], base=2)
co2 = int(split_co2[0], base=2)

print("O2:", o2)
print("CO2:", co2)
print("Second answer:", o2 * co2)
 