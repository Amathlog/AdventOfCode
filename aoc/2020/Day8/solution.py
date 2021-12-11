from pathlib import Path
import os
from typing import List, Tuple

entry_file = Path(os.path.abspath(__file__)).parent / "entry.txt"

with entry_file.open("r") as f:
    entries = f.readlines()

for i in range(len(entries)):
    if entries[i][-1] == '\n':
        entries[i] = entries[i][:-1]

def execute(entries: List[str]) -> Tuple[bool, int]:
    accumulator = 0
    pc = 0
    instructionsSeen = set()

    while pc < len(entries):
        if (pc in instructionsSeen):
            break

        instructionsSeen.add(pc)
        opCode, value = entries[pc].split(" ")
        value = int(value)

        if opCode == "nop":
            pc += 1
            continue

        if opCode == "jmp":
            pc += value
            continue

        accumulator += value
        pc += 1
        continue

    return pc == len(entries), accumulator

print("First answer:", execute(entries)[1])

# Brute force
for i in range(len(entries)):
    opCode, value = entries[i].split(" ")
    if opCode == "acc":
        continue

    saved_entry = entries[i]
    entries[i] = f"jmp {value}" if opCode == "nop" else f"nop {value}"
    
    success, acc = execute(entries)
    if success:
        print("Second answer:", acc)
        break

    entries[i] = saved_entry
