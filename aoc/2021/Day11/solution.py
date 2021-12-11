from pathlib import Path
import os
from typing import List, Tuple
from aoc.utils import neighboor_iter

entry_file = Path(os.path.abspath(__file__)).parent / "entry.txt"

with entry_file.open("r") as f:
    entries = f.readlines()

for i in range(len(entries)):
    if entries[i][-1] == '\n':
        entries[i] = entries[i][:-1]

entries = [[int(x) for x in e] for e in entries]

def simulation_step(e: List[List[int]]) -> Tuple[List[List[int]], int]:
    nb_flashes = 0
    ready_to_flash = []
    for i in range(len(e)):
        for j in range(len(e[i])):
            e[i][j] += 1
            if e[i][j] > 9:
                ready_to_flash.append((i, j))

    while len(ready_to_flash) > 0:
        i, j = ready_to_flash.pop()
        if e[i][j] == 0:
            continue

        nb_flashes += 1
        e[i][j] = 0

        for new_i, new_j in neighboor_iter(i, j, len(e), len(e[0])):
            if e[new_i][new_j] == 0:
                # Already flashed
                continue

            e[new_i][new_j] += 1

            if e[new_i][new_j] > 9:
                ready_to_flash.append((new_i, new_j))

    return e, nb_flashes


def debug_print(e: List[List[int]]):
    for x in e:
        print("".join([str(i) for i in x]))
    print()


if __name__ == "__main__":
    import copy
    entries_ = copy.deepcopy(entries)
    first_full_flash = -1

    nb_flashes = 0
    i = 0
    while True:
        entries_, temp = simulation_step(entries_)
        nb_flashes += temp
        i += 1

        if temp == 100:
            first_full_flash = i

        if i == 100:
            print("First answer:", nb_flashes)
        
        if first_full_flash != -1 and i >= 100:
            break


    print("Second answer:", first_full_flash)