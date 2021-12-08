from pathlib import Path
import os
from typing import List
from collections import defaultdict

entry_file = Path(os.path.abspath(__file__)).parent / "entry.txt"

with entry_file.open("r") as f:
    entries = f.readlines()

for i in range(len(entries)):
    if entries[i][-1] == '\n':
        entries[i] = entries[i][:-1]

entries = [x.split(" | ") for x in entries]

count = 0
for e in entries:
    digits = e[1].split(" ")
    for digit in digits:
        if len(digit) in [2, 3, 4, 7]:
            count += 1

print("First answer:", count)

segments = {
    0: [1, 2, 3, 5, 6, 7],
    1: [3, 6],
    2: [1, 3, 4, 5, 7],
    3: [1, 3, 4, 6, 7],
    4: [2, 3, 4, 6],
    5: [1, 2, 4, 6, 7],
    6: [1, 2, 4, 5, 6, 7],
    7: [1, 3, 6],
    8: [1, 2, 3, 4, 5, 6, 7],
    9: [1, 2, 3, 4, 6, 7],
}

segments_len = {x: len(v) for x,v in segments.items()}
inverse_segment_len = {v: [x for x in segments_len.keys() if segments_len[x] == v] for v in set(segments_len.values())}

def get_index(c: str):
    return ord(c) - ord("a") + 1

def map_possible_digits(e: List[str]):
    mapping = {}
    e = sorted(e, key=lambda x: len(x))

    mapping[e[0]] = 1
    mapping[e[1]] = 7
    mapping[e[2]] = 4
    mapping[e[9]] = 8

    # First we can find segment a, by finding the diff between signal of len 2 (1) and len 3 (7)
    a_segment = [c for c in e[1] if c not in e[2]][0]

    segments_cf = [c for c in e[0]]

    # By comparing all signal of len 5 (2, 3, 5), we can find segment d and g
    segments_dg = [c for c in e[3] if c in e[4] and c in e[5] and c != a_segment]

    # a, c, f, d, g is number 3
    for s in e[3:6]:
        found = True
        for c in s:
            if c != a_segment and c not in segments_cf and c not in segments_dg:
                found = False
                break

        if found:
            mapping[s] = 3
            break

    # We can find segment b by analysing digit 4
    segment_b = [c for c in e[2] if c not in segments_dg and c not in segments_cf][0]
    
    # By knowing that, we can find digit 5, and by elimination also digit 2
    for s in e[3:6]:
        found = False
        for c in s:
            if c == segment_b:
                found = True
                break

        if found:
            mapping[s] = 5
            signal_5 = s
            break

    for s in e[3:6]:
        if s in mapping.keys():
            continue
        mapping[s] = 2
        break

    # We can find digit 9 now, with segments a, b, c, d, f, g
    for s in e[6:9]:
        found = True
        for c in s:
            if c != a_segment and c != segment_b and c not in segments_cf and c not in segments_dg:
                found = False
                break

        if found:
            mapping[s] = 9
            signal_9 = s
            break

    # We can find segment c by conparing digit 7 and digit 5
    for c in e[1]:
        if c not in signal_5:
            segment_c = c
            break

    # We can find now our last 2 digits
    for s in e[6:9]:
        if s == signal_9:
            continue

        found = False
        for c in s:
            if c == segment_c:
                found = True
                break

        if found:
            mapping[s] = 0
            break

    for s in e[6:9]:
        if s in mapping.keys():
            continue
        mapping[s] = 6
        break
    
    return mapping

res = 0
for e in entries:
    signals = e[0].split(" ")
    values = e[1].split(" ")

    mapping = map_possible_digits(signals)
    mapping = {"".join(sorted(x)): v for x,v in mapping.items()}
    digit = 0
    for v in values:
        digit = digit * 10 + mapping["".join(sorted(v))]

    res += digit

print("Second answer:", res)
