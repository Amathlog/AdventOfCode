from pathlib import Path
import os

entry_file = Path(os.path.abspath(__file__)).parent / "entry.txt"

with entry_file.open("r") as f:
    entries = f.readlines()

# Add a final blank line if missing
if entries[-1] != "\n":
    entries += "\n"

count = 0
temp = set()
all_data = [[]]
for entry in entries:
    # Strip \n
    entry = entry[:-1]
    if entry == "":
        count += len(temp)
        temp = set()
        all_data[-1] = sorted(all_data[-1], key=lambda x: len(x))
        all_data.append([])
        continue
    all_data[-1].append(set())
    for c in entry:
        all_data[-1][-1].add(c)
        temp.add(c)

print("Result first question:", count)

count = 0
for data in all_data[:-1]:
    if len(data) == 1:
        count += len(data[0])
        continue

    temp = 0
    for c in data[0]:
        all_found = True
        for s in data[1:]:
            if c not in s:
                all_found = False
                break
        if all_found:
            temp += 1
    count += temp

print("Result second question:", count)