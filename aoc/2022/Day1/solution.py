from pathlib import Path
import os
import copy

from collections import namedtuple

entry_file = Path(os.path.abspath(__file__)).parent / "entry.txt"
example_file = Path(os.path.abspath(__file__)).parent / "example.txt"

with entry_file.open("r") as f:
    entries = f.readlines()

for i in range(len(entries)):
    if entries[i][-1] == '\n':
        entries[i] = entries[i][:-1]


Entry = namedtuple("Entry", ['index', 'total_calories'])

total_calories = []
current_sum = 0
current_index = 0

for item in entries:
    if (item == ""):
        total_calories.append(Entry(current_index, current_sum))
        current_sum = 0
        current_index += 1
        continue

    current_sum += int(item)

total_calories = sorted(total_calories, key=lambda x: x[1], reverse=True)

print(f"Part 1: Elf number {total_calories[0].index} holds the most calories {total_calories[0].total_calories}")

three_most_calories = total_calories[:3]

print(f"Part 2: The three elves that has the most calories are " + ",".join([str(t.index) for t in three_most_calories]) 
    + f" for a total of {sum([t.total_calories for t in three_most_calories])}")