from pathlib import Path
import os

entry_file = Path(os.path.abspath(__file__)).parent / "entry.txt"

with entry_file.open("r") as f:
    entries = f.readlines()

for i in range(len(entries)):
    if entries[i][-1] == '\n':
        entries[i] = entries[i][:-1]
    entries[i] = int(entries[i])

if __name__ == "__main__":
    # Exo 1
    count = 0
    for i in range(1, len(entries)):
        if entries[i] > entries[i-1]:
            count += 1

    print("First answer:", count)

    # Exo 2
    count = 0
    for i in range(3, len(entries)):
        if sum(entries[i-3:i]) < sum(entries[i-2:i+1]):
            count += 1

    print("Second answer:", count)
