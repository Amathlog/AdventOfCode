from pathlib import Path
import os

entry_file = Path(os.path.abspath(__file__)).parent / "entry.txt"

with entry_file.open("r") as f:
    entries = set([int(i) for i in f.readlines()])

target = 2020

# case 2
for i in entries:
    other = target - i
    if other < 0:
        continue

    if other in entries:
        print(f"{i} * {other} = {i*other}")
        break

# case 3
found = False
for i in entries:
    if found:
        break

    for j in entries:
        if i == j:
            continue

        other = target - i - j
        if other < 0:
            continue

        if other in entries:
            print(f"{i} * {j} * {other} = {i*j*other}")
            found = True
            break