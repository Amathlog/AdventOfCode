from pathlib import Path
import os
import copy

entry_file = Path(os.path.abspath(__file__)).parent / "entry.txt"
example_file = Path(os.path.abspath(__file__)).parent / "example.txt"

with example_file.open("r") as f:
    entries = f.readlines()

for i in range(len(entries)):
    if entries[i][-1] == '\n':
        entries[i] = entries[i][:-1]
