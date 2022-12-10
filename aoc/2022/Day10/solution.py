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

cycle = 1
curr_inst = 0
is_add = False
incr = 0
sum_signals = 0
cycles_to_look_for = set([20, 60, 100, 140, 180, 220])
x = 1

def check():
    res = 0
    if cycle in cycles_to_look_for:
        res = cycle * x

    # Also render
    current_pixel = (cycle - 1) % 40
    char = "#" if abs(current_pixel - x) <= 1 else " "
    print(char, end="")
    if current_pixel == 39:
        print()

    return res

while True:
    was_add = is_add
    if not is_add:
        inst = entries[curr_inst]
        if inst != "noop":
            is_add = True
            incr = int(inst.split(" ")[1])
        else:
            curr_inst += 1

    sum_signals += check()
    cycle += 1

    if was_add:
        x += incr
        is_add = False
        curr_inst += 1

    if curr_inst >= len(entries):
        break

print("Part 1: Sum of signals ", sum_signals)
