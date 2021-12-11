from pathlib import Path
import os

entry_file = Path(os.path.abspath(__file__)).parent / "entry.txt"

with entry_file.open("r") as f:
    entries = f.readlines()

for i in range(len(entries)):
    if entries[i][-1] == '\n':
        entries[i] = entries[i][:-1]

    entries[i] = int(entries[i])

entries = sorted(entries)
# We also need to take into account the outlet (jolt 0)
# and the device (max jolt + 3)
entries.insert(0, 0)
entries.append(entries[-1] + 3)

diffs = [0, 0, 0]

for i in range(1, len(entries)):
    diff = entries[i] - entries[i-1]
    diffs[diff - 1] += 1

print("First answer:", diffs[0] * diffs[2])

# First construct the tree, then visit all nodes from smallest to biggest
# in order to compute the possibilities
import copy
memory = {0: []}
max_range = 3
for i in range(len(entries) - 1, 0, -1):
    value = entries[i]
    connections = []
    idx = i - 1
    while idx >= 0 and value - entries[idx] <= max_range:
        connections.append(entries[idx])
        idx -= 1

    memory[value] = copy.deepcopy(connections)
    
res = {0: 1}
for e in entries[1:]:
    res[e] = sum([res[x] for x in memory[e]])

print(res[entries[-1]])
