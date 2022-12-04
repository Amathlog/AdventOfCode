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

def get_priority(c: str) -> int:
    if ord(c) <= ord('Z'):
        return 27 + ord(c) - ord('A')
    
    return ord(c) - ord('a') + 1

def find_common_type(input: str) -> str:
    left, right = input[:len(input) // 2], input[len(input) // 2:]
    left, right = set(list(left)), set(list(right))

    return list(left.intersection(right))[0]

def find_priority_common_type(input: str) -> int:
    return get_priority(find_common_type(input))

def find_common_type_three(inputs: tuple[str, str, str]) -> str:
    all_sets = [set(list(i)) for i in inputs]
    return list(all_sets[0].intersection(all_sets[1].intersection(all_sets[2])))[0]

def find_priority_common_type_three(inputs: tuple[str, str, str]) -> str:
    return get_priority(find_common_type_three(inputs))

print(f"Part 1: Sum of priorities = {sum([find_priority_common_type(e) for e in entries])}")

groups = (entries[3*i:3*(i+1)] for i in range(len(entries) // 3))
print(f"Part 2: Sum of priorities = {sum([find_priority_common_type_three(g) for g in groups])}")