from pathlib import Path
import os
from typing import List, Tuple
import numpy as np

entry_file = Path(os.path.abspath(__file__)).parent / "entry.txt"

with entry_file.open("r") as f:
    entries = f.readlines()

for i in range(len(entries)):
    if entries[i][-1] == '\n':
        entries[i] = entries[i][:-1]

earliest_timestamp = int(entries[0])
bus_ids = [(int(x), i) for i, x in enumerate(entries[1].split(",")) if x != "x"]


mods = [x[0] - (earliest_timestamp % x[0]) for x in bus_ids]
min_mod = np.argmin(mods)

print("First answer:", bus_ids[min_mod][0] * mods[min_mod])

def is_t_valid(t: int, ids):
    valid = True
    for x, i in ids:
        if (t + i) % x != 0:
            valid = False
            break

    return valid

def compute_second_answer(ids: List[Tuple[int, int]]) -> int:
    curr_incr = 1
    t = 0
    for id, offset in ids:
        modulo_seen = set()
        while True:
            mod = (t + offset) % id
            # If this is true, the problem is impossible
            if mod in modulo_seen:
                return -1
            
            if mod == 0:
                curr_incr *= id
                break
            
            modulo_seen.add(mod)
            t += curr_incr
    return t


print("Second answer:", compute_second_answer(bus_ids))