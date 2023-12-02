from pathlib import Path
import sys
import os
import urllib.request

template = """from pathlib import Path
import os
import copy
from typing import List, Tuple, Dict
from aoc.common.parse_entry import parse_all

entries, example_entries = parse_all(__file__, "entry.txt", "example.txt")
"""

folder = Path(os.path.abspath(__file__)).parent / "aoc"

if len(sys.argv) < 3:
    year_number = max([item.name for item in folder.iterdir() if item.is_dir()])
    year = folder / year_number
    day = max([int(item.name[3:]) for item in year.iterdir() if item.is_dir()])
    day_number = str(day + 1)
    pass
else:
    year_number = sys.argv[1]
    year = folder / year_number
    day_number = sys.argv[2]

day = year / ("Day" + day_number)
entry = day / "entry.txt"
example = day / "example.txt"
solution = day / "solution.py"

day.mkdir(parents=True, exist_ok=True)

with solution.open('w') as f:
    f.write(template)

entry.touch()
example.touch()