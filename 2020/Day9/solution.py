from pathlib import Path
import os
from collections import deque

entry_file = Path(os.path.abspath(__file__)).parent / "entry.txt"

with entry_file.open("r") as f:
    entries = f.readlines()

for i in range(len(entries)):
    if entries[i][-1] == '\n':
        entries[i] = entries[i][:-1]

    entries[i] = int(entries[i])

n = 25

previous_numbers = deque(entries[:n])
weakness_value = 0

for i in range(n, len(entries)):
    new_value = entries[i]

    found = False
    for x in range(len(previous_numbers)):
        for y in range(x, len(previous_numbers)):
            if previous_numbers[x] + previous_numbers[y] == new_value:
                found = True
                break
        if found:
            break

    if not found:
        weakness_value = new_value
        break

    previous_numbers.popleft()
    previous_numbers.append(new_value)

print("First answer:", weakness_value)

found = False
for i in range(len(entries)):
    weakness_sum = 0
    min_weakness = 99999999999999999999999999999
    max_weakness = 0

    for j in range(i, len(entries)):
        weakness_sum += entries[j]
        if entries[j] < min_weakness:
            min_weakness = entries[j]
        if entries[j] > max_weakness:
            max_weakness = entries[j]

        if weakness_sum >= weakness_value:
            found = weakness_value == weakness_sum
            break

    if found:
        break

print("Second answer:", min_weakness + max_weakness)
