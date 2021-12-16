from pathlib import Path
import sys
import os
import urllib.request

year_number = sys.argv[1]
day_number = sys.argv[2]

template = """from pathlib import Path
import os
import copy

entry_file = Path(os.path.abspath(__file__)).parent / "entry.txt"
example_file = Path(os.path.abspath(__file__)).parent / "example.txt"

with example_file.open("r") as f:
    entries = f.readlines()

for i in range(len(entries)):
    if entries[i][-1] == '\\n':
        entries[i] = entries[i][:-1]
"""

folder = Path(os.path.abspath(__file__)).parent / "aoc"

year = folder / year_number
day = year / ("Day" + day_number)
entry = day / "entry.txt"
example = day / "example.txt"
solution = day / "solution.py"

day.mkdir(parents=True, exist_ok=True)

with solution.open('w') as f:
    f.write(template)

entry.touch()
example.touch()