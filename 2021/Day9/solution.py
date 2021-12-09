from pathlib import Path
import os
from typing import List, Tuple

entry_file = Path(os.path.abspath(__file__)).parent / "entry.txt"

with entry_file.open("r") as f:
    entries = f.readlines()

for i in range(len(entries)):
    if entries[i][-1] == '\n':
        entries[i] = entries[i][:-1]

entries = [[int(x) for x in e] for e in entries]

def get_lowest_point(e: List[List[int]], x_: int, y_: int) -> Tuple[Tuple[int, int], bool]:
    lowest_point = (x_, y_)
    lowest_value = e[x_][y_]
    for next_x, next_y in ((x_ + 1, y_), (x_, y_ + 1), (x_ - 1, y_), (x_, y_ - 1)):
        if next_x < 0 or next_y < 0 or next_x >= len(e) or next_y >= len(e[0]):
            continue

        if e[next_x][next_y] < lowest_value:
            lowest_value = e[next_x][next_y]
            lowest_point = (next_x, next_y)

    return lowest_point, lowest_value == 9

def is_lowest_point(e: List[List[int]], x_: int, y_: int) -> bool:
    lowest_point, all_equal = get_lowest_point(e, x_, y_)
    return lowest_point == (x_, y_) and not all_equal

def inverse_flowing(e: List[List[int]], x_: int, y_: int):
    stack = [(x_, y_)]
    basin = set()
    while len(stack) > 0:
        curr = stack.pop()
        x, y = curr
        if curr in basin:
            continue

        if x < 0 or y < 0 or x >= len(e) or y >= len(e[0]):
            continue

        if e[x][y] == 9:
            continue
        
        basin.add(curr)
        stack.extend([(x + 1, y), (x, y + 1), (x - 1, y), (x, y - 1)])

    return len(basin)


if __name__ == "__main__":
    sum = 0
    lowest_points = []
    for x in range(len(entries)):
        for y in range(len(entries[0])):
            if is_lowest_point(entries, x, y):
                sum += 1 + entries[x][y]
                lowest_points.append((x, y))

    print("First answer:", sum)

    basins = []
    for p in lowest_points:
        basins.append(inverse_flowing(entries, p[0], p[1]))

    basins = sorted(basins, reverse=True)
    print("Second answer:", basins[0] * basins[1] * basins[2])