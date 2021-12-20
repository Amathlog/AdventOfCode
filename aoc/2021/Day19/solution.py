from collections import defaultdict
from pathlib import Path
import os
import copy
from typing import Dict, List, Optional, Tuple
import numpy as np

DistanceDict = Dict[float, List[Tuple[int,int]]]

entry_file = Path(os.path.abspath(__file__)).parent / "entry.txt"
example_file = Path(os.path.abspath(__file__)).parent / "example.txt"

with entry_file.open("r") as f:
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

def compute_look_at(forward: np.ndarray, up: np.ndarray, p: np.ndarray, p_: np.ndarray):
    # Look at matrix is like this:
    # | a d g -(alpha * a + beta * b + gamma * c) |
    # | b e h -(alpha * d + beta * e + gamma * f) |
    # | c f i -(alpha * g + beta * h + gamma * i) |
    # | 0 0 0                  1                  |
    #
    # p is the point in ref 0, p = (x, y, z)
    # p_ is the point in ref 1, p_ = (x_, y_, z_)
    # T is the translation vector T = (alpha, beta, gamma)
    # We have those equations:
    # p_ = M @ p
    # 
    # a*x + d*y + g*z - x_ = alpha * a + beta * b + gamma * c
    # b*x + e*y + h*z - y_ = alpha * d + beta * e + gamma * f
    # c*x + f*y + i*z - z_ = alpha * g + beta * h + gamma * i
    # If we constraint forward and up, to be only along a given axis (x, y or z axis), it also constraint right to a single axis.
    # it means that in (a,b,c) only one is not 0. Same for (d,e,f) and (g, h, i)
    # They are not randomly 0 either, it will simplify the equation to the right and let only 3 equations
    # One for alpha, one for beta and one for gamma

    right = np.cross(up, forward)
    rotation_matrix = np.ones((3,3), dtype=np.int32)
    rotation_matrix[:, 0] = forward
    rotation_matrix[:, 1] = right
    rotation_matrix[:, 2] = up

    x_value, y_value, z_value = rotation_matrix @ p[:3] - p_[:3]
    translation = np.array([1,2,3], dtype=np.int32)
    
    translation_x = np.dot(translation, forward)
    translation_y = np.dot(translation, right)
    translation_z = np.dot(translation, up)

    for t, v in zip([translation_x, translation_y, translation_z], [x_value, y_value, z_value]):
        translation[abs(t) - 1] = v if t > 0 else -v

    return look_at(forward, up, translation)

positive_x = np.array([1, 0, 0])
negative_x = np.array([-1, 0, 0])
positive_y = np.array([0, 1, 0])
negative_y = np.array([0, -1, 0])
positive_z = np.array([0, 0, 1])
negative_z = np.array([0, 0, -1])


def compute_all_distances(points: List[np.ndarray]) -> DistanceDict:
    res = {}
    for i, p1 in enumerate(points):
        for j, p2 in enumerate(points[i+1:]):
            l2_norm = np.linalg.norm(p1 - p2, ord=2)
            if l2_norm in res:
                assert(False) # Not good
            res[l2_norm] = (i,i+1+j)

    return res

def find_overlapping(distances1: DistanceDict, distances2: DistanceDict, min_match: int = 12) -> Dict[int, int]:
    same_distances = set(distances1.keys()).intersection(set(distances2.keys()))
    if len(same_distances) < ((min_match-1) * (min_match) // 2):
        return None

    # Count how often each point appears
    all_points1, all_points2 = defaultdict(int), defaultdict(int)
    for dist in same_distances:
        p1, p2 = distances1[dist]
        all_points1[p1] += 1
        all_points1[p2] += 1

        p_1, p_2 = distances2[dist]
        all_points2[p_1] += 1
        all_points2[p_2] += 1

    # We know that at least `min_match` points that are detected by both scanners.
    # Find the mapping between them by doing set intersections between same distances.
    mapping_1_to_2 = {}
    for dist in same_distances:
        p1, p2 = distances1[dist]

        # A good point should appear multiple times, at least min_match - 1
        if all_points1[p1] < min_match - 1 or all_points1[p2] < min_match - 1:
            continue

        new_set = set(distances2[dist])

        if p1 not in mapping_1_to_2:
            mapping_1_to_2[p1] = set(new_set)
        else:
            mapping_1_to_2[p1].intersection_update(new_set)

        if p2 not in mapping_1_to_2:
            mapping_1_to_2[p2] = set(new_set)
        else:
            mapping_1_to_2[p2].intersection_update(new_set)

    return {k: v.pop() for k, v in mapping_1_to_2.items() if len(v) == 1}


if __name__ == "__main__":
    scanners = []
    for l in entries:
        if l[0:2] == "--":
            scanners.append([])
            continue
        if l == "":
            continue
        scanners[-1].append(np.concatenate([[int(v) for v in l.split(',')], [1]]))

    distances = []
    for s in scanners:
        distances.append(compute_all_distances(s))

    all_points = set([tuple(p) for p in scanners[0]])
    transforms_to_scanner_0_ref = {0: np.identity(4, dtype=np.int32)}

    scanners_to_check = [0]

    while len(scanners_to_check) > 0:
        curr = scanners_to_check.pop(0)

        for other in range(len(scanners)):
            if other in transforms_to_scanner_0_ref:
                # Already found
                continue

            mapping_first_to_second = find_overlapping(distances[curr], distances[other])
            if mapping_first_to_second is None:
                continue

            # Get the first 2 points
            # Test all the possible look at matrix, that will work for all points
            # (Can be done with linear regression, but I'm a noob)
            p, p_ = list(mapping_first_to_second.items())[0]
            p = scanners[curr][p]
            p_ = scanners[other][p_]

            # We want to transform p_ into p (find the matrix that will transform ref 2 to ref 1)
            all_vectors = [positive_x, positive_y, positive_z, negative_x, negative_y, negative_z]
            found = False
            la = None
            for forward in all_vectors:
                for up in all_vectors:
                    if np.dot(forward, up) != 0:
                        continue

                    tentative_look_at = compute_look_at(forward, up, p_, p)
                    match = True
                    for p1, p2 in mapping_first_to_second.items():
                        p1 = scanners[curr][p1]
                        p2 = scanners[other][p2]

                        transformed = tentative_look_at @ p2
                        if (transformed != p1).any():
                            match = False
                            break

                    if not match:
                        continue

                    # We got a match!
                    la = tentative_look_at
                    found = True

                if found:
                    break

            assert(found)
            # Store the tranformation to scanner 0
            transforms_to_scanner_0_ref[other] = transforms_to_scanner_0_ref[curr] @ la

            # And finally convert all the points of this scanner in scanner 0 ref
            for p in scanners[other]:
                new_p = transforms_to_scanner_0_ref[other] @ p
                all_points.add(tuple(new_p))

            scanners_to_check.append(other)

    print("First answer:", len(all_points))

    # Now that we have the position of all the scanners relative to scanner 0, we can try to find the maximum distance between them
    max_dist = 0
    for i in range(len(scanners)):
        for j in range(len(scanners)):
            if i == j:
                continue

            pos_i = transforms_to_scanner_0_ref[i][:3,3]
            pos_j = transforms_to_scanner_0_ref[j][:3,3]

            dist = int(np.linalg.norm(pos_i - pos_j, ord=1))
            if dist > max_dist:
                max_dist = dist

    print("Second answer:", max_dist)
