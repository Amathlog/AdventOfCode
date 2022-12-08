from pathlib import Path
import os
import copy

entry_file = Path(os.path.abspath(__file__)).parent / "entry.txt"
example_file = Path(os.path.abspath(__file__)).parent / "example.txt"

with entry_file.open("r") as f:
    entries = f.readlines()

for i in range(len(entries)):
    if entries[i][-1] == '\n':
        entries[i] = entries[i][:-1]

grid = [[int(i) for i in e] for e in entries]

height = len(grid)
width = len(grid[0])

distances = [[1 for j in range(width)] for i in range(height)]
visible = set()

for i, line in enumerate(grid):
    current_max = -1
    cache = {}
    for j, value in enumerate(line):
        dists = [v for k,v in cache.items() if k >= value]
        if len(dists) == 0:
            distances[i][j] *= j
        else:
            distances[i][j] *= j - max(dists)

        cache[value] = j
    
        if value > current_max:
            visible.add((i, j))
            current_max = value

    current_max = -1
    cache = {}
    for j, value in enumerate(line[::-1]):
        index = width - j - 1

        dists = [v for k,v in cache.items() if k >= value]
        if len(dists) == 0:
            distances[i][index] *= j
        else:
            distances[i][index] *= j - max(dists)

        cache[value] = j

        if value > current_max:
            visible.add((i, index))
            current_max = value

for j in range(width):
    current_max = -1
    cache = {}
    for i in range(height):
        value = grid[i][j]
        dists = [v for k,v in cache.items() if k >= value]
        if len(dists) == 0:
            distances[i][j] *= i
        else:
            distances[i][j] *= i - max(dists)

        cache[value] = i

        if value > current_max:
            visible.add((i, j))
            current_max = value

    current_max = -1
    cache = {}

    for i in range(height):
        index = height - i - 1
        value = grid[index][j]

        dists = [v for k,v in cache.items() if k >= value]
        if len(dists) == 0:
            distances[index][j] *= i
        else:
            distances[index][j] *= i - max(dists)

        cache[value] = i

        if value > current_max:
            visible.add((index, j))
            current_max = value

print(f"Part 1: Number of visible trees: {len(visible)}")

print(f"Part 2: Max scenic score: {max((max(d) for d in distances))}")