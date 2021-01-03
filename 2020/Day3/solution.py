from pathlib import Path
import os
from functools import reduce

entry_file = Path(os.path.abspath(__file__)).parent / "entry.txt"

class Slope:
    def __init__(self, buffer):
        self.width = len(buffer[0]) - 1
        self.height = len(buffer)
        # Remove `\n` at the end
        self.data = [[c == '#' for c in s[:-1]] for s in buffer]

    def encountered_trees(self, start_position: tuple, rule: tuple):
        x, y = start_position
        count = 0
        while y < self.height:
            if self.data[y][x % self.width]:
                count += 1
            x += rule[0]
            y += rule[1]
        return count

with entry_file.open("r") as f:
    slope = Slope(f.readlines())

print("Nb trees encountered:", slope.encountered_trees((0,0), (3,1)))

# second part
collisions = []
for rule in [(1,1), (3,1), (5,1), (7,1), (1,2)]:
    collisions.append(slope.encountered_trees((0,0), rule))

print("All collisions:", collisions)
print("Res:", reduce(lambda x,y: x*y, collisions))
