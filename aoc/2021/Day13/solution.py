from pathlib import Path
import os
import copy
from typing import List

entry_file = Path(os.path.abspath(__file__)).parent / "entry.txt"
example_file = Path(os.path.abspath(__file__)).parent / "example.txt"

with entry_file.open("r") as f:
    entries = f.readlines()

for i in range(len(entries)):
    if entries[i][-1] == '\n':
        entries[i] = entries[i][:-1]

class Grid:
    def __init__(self, e: List[str]):
        self.dots = set()
        self.size_x = 0
        self.size_y = 0
        for e_ in e:
            x, y = e_.split(",")
            x = int(x)
            y = int(y)

            self.dots.add((x, y))

            if x + 1 > self.size_x:
                self.size_x = x + 1
            if y + 1 > self.size_y:
                self.size_y = y + 1

    def __repr__(self) -> str:
        res = []
        for y in range(self.size_y):
            res.append([])
            for x in range(self.size_x):
                res[-1].append(".")

        for dot in self.dots:
            res[dot[1]][dot[0]] = "#"

        return "\n".join(["".join(e) for e in res])

    def fold(self, axis_x: bool, index: int):
        new_dots = set()
        for d in self.dots:
            if axis_x and d[0] > index:
                new_dot = (self.size_x - d[0] - 1, d[1])
            elif not axis_x and d[1] > index:
                new_dot = (d[0], self.size_y - d[1] - 1)
            else:
                new_dot = d

            new_dots.add(new_dot)

        self.dots = new_dots
        if axis_x:
            self.size_x //= 2
        else:
            self.size_y //= 2

if __name__ == "__main__":
    for i in range(len(entries)):
        if entries[i] == "":
            break

    dots = entries[:i]
    folds = entries[i+1:]

    grid = Grid(dots)
    
    for i, f in enumerate(folds):
        _, __, info = f.split(" ")
        axis, index = info.split("=")
        axis_x = axis == "x"
        index = int(index)
        grid.fold(axis_x, index)

        if i == 0:
            print("First answer:", len(grid.dots))

    print(grid)