from pathlib import Path
import os

entry_file = Path(os.path.abspath(__file__)).parent / "entry.txt"

with entry_file.open("r") as f:
    entries = f.readlines()

for i in range(len(entries)):
    if entries[i][-1] == '\n':
        entries[i] = entries[i][:-1]


x = 0
y = 0

for e in entries:
    dir, i = e.split(" ")
    i = int(i)

    if dir == "forward":
        x += i
    elif dir == "down":
        y += i
    else:
        y -= i

print("First anwser:", x * y)

x = 0
y = 0
aim = 0

for e in entries:
    dir, i = e.split(" ")
    i = int(i)

    if dir == "forward":
        x += i
        y += i * aim
    elif dir == "down":
        aim += i
    else:
        aim -= i

print("Second anwser:", x * y)