from pathlib import Path
import os
from typing import Optional, Tuple

entry_file = Path(os.path.abspath(__file__)).parent / "entry.txt"

with entry_file.open("r") as f:
    entries = f.readlines()

for i in range(len(entries)):
    if entries[i][-1] == '\n':
        entries[i] = entries[i][:-1]

def get_corresponding_closer(s: str):
    if s == "{":
        return "}"
    if s == "[":
        return "]"
    if s == "(":
        return ")"
    if s == "<":
        return ">"

def find_corrupted_character_or_fill(e: str) -> Tuple[bool, str]:
    stack_chunk = []
    for c in e:
        is_opening = c in ["{", "[", "(", "<"]
        if is_opening:
            stack_chunk.append(c)
            continue

        if len(stack_chunk) == 0:
            return True, c

        latest = stack_chunk.pop()
        if c != get_corresponding_closer(latest):
            return True, c

    return False, "".join([get_corresponding_closer(c) for c in reversed(stack_chunk)])

def get_score_1(c: str) -> int:
    if c == ")":
        return 3
    if c == "]":
        return 57
    if c == "}":
        return 1197
    if c == ">":
        return 25137

    return 0

def get_score_2(c: str) -> int:
    if c == ")":
        return 1
    if c == "]":
        return 2
    if c == "}":
        return 3
    if c == ">":
        return 4
    
    return 0

if __name__ == "__main__":
    score_1 = 0
    score_2 = []
    for e in entries:
        corrupted, res = find_corrupted_character_or_fill(e)
        if corrupted:
            score_1 += get_score_1(res)
        else:
            score_2.append(0)
            for c in res:
                score_2[-1] = score_2[-1] * 5 + get_score_2(c)

    print("First answer:", score_1)
    print("Second answer:", sorted(score_2)[len(score_2) // 2]) 