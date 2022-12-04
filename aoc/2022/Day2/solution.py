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

def score(input:str) -> int:
    other_move, _, your_move = input

    res = ord(your_move) - ord('X') + 1
    other_res = ord(other_move) - ord('A') + 1

    showdown = res - other_res

    if (showdown == 0):
        final = res + 3 # draw
    elif (showdown == 1 or showdown == -2):
        final = res + 6 # win
    else:
        final = res # lose

    return final

def score_2(input:str) -> int:
    other_move, _, showdown_res = input

    other_res = ord(other_move) - ord('A') + 1

    if (showdown_res == 'X'):
        res = 0 + (other_res + 1) % 3 + 1 # lose
    elif (showdown_res == 'Y'):
        res = 3 + other_res # draw
    else:
        res = 6 + other_res % 3 + 1

    return res


print(f"Part 1: Final score is {sum((score(e) for e in entries))}")

print(f"Part 1: Final score is {sum((score_2(e) for e in entries))}")
