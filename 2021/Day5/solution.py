from pathlib import Path
import os
from collections import defaultdict
from typing import Dict

entry_file = Path(os.path.abspath(__file__)).parent / "entry.txt"

with entry_file.open("r") as f:
    entries = f.readlines()

for i in range(len(entries)):
    if entries[i][-1] == '\n':
        entries[i] = entries[i][:-1]

segments = []
for e in entries:
    pt1, pt2 = e.split(" -> ")
    pt1 = [int(x) for x in pt1.split(",")]
    pt2 = [int(x) for x in pt2.split(",")]
    segments.append((pt1, pt2))

def fill_grid(with_diagonal: bool) -> Dict:
    grid = defaultdict(lambda: 0)
    for segment in segments:
        x1, y1 = segment[0]
        x2, y2 = segment[1]
        x_step = 1 if x1 < x2 else -1
        y_step = 1 if y1 < y2 else -1

        x_range = range(x1, x2 + x_step, x_step)
        y_range = range(y1, y2 + y_step, y_step)

        if y1 == y2:
            # Horizontal
            for x in x_range:
                grid[(x, y1)] += 1
        elif x1 == x2:
            # Vertical
            for y in y_range:
                grid[(x1, y)] += 1
        elif with_diagonal:
            # Diagonal
            for x, y in zip(x_range, y_range):
                grid[(x, y)] += 1

    return grid

count = 0
for v in fill_grid(False).values():
    if v >= 2:
        count += 1

print("First answer", count)

count = 0
for v in fill_grid(True).values():
    if v >= 2:
        count += 1

print("Second answer", count)