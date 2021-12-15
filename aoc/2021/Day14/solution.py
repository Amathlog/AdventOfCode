from pathlib import Path
import os
import collections
from typing import Tuple

entry_file = Path(os.path.abspath(__file__)).parent / "entry.txt"
example_file = Path(os.path.abspath(__file__)).parent / "example.txt"

with entry_file.open("r") as f:
    entries = f.readlines()

for i in range(len(entries)):
    if entries[i][-1] == '\n':
        entries[i] = entries[i][:-1]

starting_list = entries[0]

combinaisons = entries[2:]
rules = {}
for x in combinaisons:
    pair, new = x.split(" -> ")
    rules[pair] = (pair[0] + new, new + pair[1])
pairs = collections.defaultdict(int)


for i in range(1, len(starting_list)):
    pairs[starting_list[i-1:i+1]] += 1

def update(p: dict, r: dict) -> dict:
    new_pairs = collections.defaultdict(int)
    for pair, value in p.items():
        new_pairs[rules[pair][0]] += value
        new_pairs[rules[pair][1]] += value

    return new_pairs

def count_elements(p: dict) -> Tuple[str, str]:
    res = collections.defaultdict(int)
    # Each item will be counted twice (since they appear in two pairs)
    # Except the left most and right most (cf comment below)
    for pair, value in p.items():
        res[pair[0]] += value
        res[pair[1]] += value

    # Left most and right most letter has count only once, so add them here
    # Since we only add letter between two letters, the left most and right most
    # letter are always the same, and can be taken from the starting list.
    res[starting_list[0]] += 1
    res[starting_list[-1]] += 1

    min_char = ""
    min_value = -1
    max_char = ""
    max_value = -1

    for c, v in res.items():
        if min_value == -1 or v < min_value:
            min_char = c
            min_value = v
        if max_value == -1 or v > max_value:
            max_char = c
            max_value = v

    return min_char, min_value // 2, max_char, max_value // 2


for _ in range(10):
    pairs = update(pairs, rules)

min_char, min_value, max_char, max_value = count_elements(pairs)
print(f"First answer: min: {min_char}, {min_value} ; max: {max_char}, {max_value} -> {max_value - min_value}")

for _ in range(30):
    pairs = update(pairs, rules)

min_char, min_value, max_char, max_value = count_elements(pairs)
print(f"Second answer: min: {min_char}, {min_value} ; max: {max_char}, {max_value} -> {max_value - min_value}")