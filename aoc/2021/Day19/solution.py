from pathlib import Path
import os
import copy
from typing import Optional, Tuple
import numpy as np
from numpy.core.defchararray import split

entry_file = Path(os.path.abspath(__file__)).parent / "entry.txt"
example_file = Path(os.path.abspath(__file__)).parent / "example.txt"

with example_file.open("r") as f:
    entries = f.readlines()

for i in range(len(entries)):
    if entries[i][-1] == '\n':
        entries[i] = entries[i][:-1]

def look_at(forward: np.ndarray, up: np.ndarray, translation: np.ndarray, dim: int = 3) -> np.ndarray:
    right = np.cross(up, forward)
    res = np.zeros((dim + 1, dim + 1), dtype=np.int32)
    res[:dim, 0] = forward
    res[:dim, 1] = right
    res[:dim, 2] = up
    res[0, 3] = -np.dot(translation, forward)
    res[1, 3] = -np.dot(translation, right)
    res[2, 3] = -np.dot(translation, up)
    res[3, 3] = 1

    return res

positive_x = np.array([1, 0, 0])
negative_x = np.array([-1, 0, 0])
positive_y = np.array([0, 1, 0])
negative_y = np.array([0, -1, 0])
positive_z = np.array([0, 0, 1])
negative_z = np.array([0, 0, -1])

# Try 2 points in ref 1 and ref 2. If they correspond to the same
# point (p1 in ref1 is p_1 in ref2 and p2 in ref1 is p_2 in ref2)
# return a matrix to transform ref1 in ref2
# Else return None
def is_same_beacons(p1, p2, p_1, p_2) -> Optional[np.ndarray]:
    temp = p1 - p2
    temp_ = p_1 - p_2

    temp = temp[:3]
    temp_ = temp_[:3]

    forward, right, up = None, None, None
    if (temp == 0).any():
        return None

    coeff = temp_ / temp

    if (np.abs(coeff) != 1).any():
        return None

    forward = positive_x if coeff[0] > 0 else negative_x
    right = positive_y if coeff[1] > 0 else negative_y
    up = positive_z if coeff[2] > 0 else negative_z

    translation = p_1[:3] * coeff - p1[:3]

    return look_at(forward, up, translation)        

if __name__ == "__main__":
    scanners = []
    for l in entries:
        if l[0:2] == "--":
            scanners.append([])
            continue
        if l == "":
            continue
        scanners[-1].append(np.concatenate([[int(v) for v in l.split(',')], [1]]))

    all_beacons = {hash(p.tobytes()): p for p in scanners[0]}

    # We want to find all the beacons, relative to scanner 0
    # To do so, we will find all the overlapping scanners with scanner 0.
    # Then we can find the overlapping one with those, and then again
    # until we find all the beacons.
    # We keep a map between scanner 0 and the other ones

    scanner0_to_others = {0: np.identity(4, dtype=np.int32)}
    scanners = scanners[:2]

    list_of_overlap = [(0, scanners[0])]
    number_of_matches = 12
    while len(list_of_overlap) > 0:
        idx, current_scanner = list_of_overlap.pop()
        for other_idx, other in enumerate(scanners):
            if other_idx in scanner0_to_others:
                continue

            nb_match = 0
            la = None
            match = False
            all_la = {}
            for i in range(len(current_scanner)):
                for j in range(i + 1, len(current_scanner)):
                    for i_ in range(len(current_scanner)):
                        for j_ in range(i_ + 1, len(current_scanner)):
                            la = is_same_beacons(other[i_], other[j_], current_scanner[i], current_scanner[j])
                            if la is None:
                                continue

                            hash_la = hash(la.tobytes())
                            if hash_la in all_la:
                                all_la[hash_la][1] += 1
                            else:
                                all_la[hash_la] = [la, 1]

                            if all_la[hash_la][1] == number_of_matches:
                                match = True
                                break

                        if match:
                            break
                    if match:
                        break
                if match:
                    break

            if match:
                scanner0_to_others[other_idx] = scanner0_to_others[idx] @ la
                for p in other:
                    new_p = scanner0_to_others[other_idx] @ p
                    all_beacons[hash(new_p.tobytes())] = new_p

                list_of_overlap.append((other_idx, other))

print(len(all_beacons))
