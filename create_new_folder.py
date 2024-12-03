from pathlib import Path
import sys
import os

template = """import copy
from typing import List, Tuple, Dict, Optional, Set
from aoc.common.parse_entry import parse_all
from aoc.common.utils import profile

entries, example_entries = parse_all(__file__, "entry.txt", "example.txt")

@profile
def part_one(entry: List[str]) -> int:
    return 0

@profile
def part_two(entry: List[str]) -> int:
    return 0


if __name__ == "__main__":
    print("Part 1 example:", part_one(example_entries))
    print("Part 1 entry:", part_one(entries))

    print("Part 2 example:", part_two(example_entries))
    print("Part 2 entry:", part_two(entries))
"""

folder = Path(os.path.abspath(__file__)).parent / "aoc"

if len(sys.argv) < 3:
    year_number = max([item.name for item in folder.iterdir() if item.is_dir() and item.name.isnumeric()])
    year = folder / year_number
    day = max([int(item.name[3:]) for item in year.iterdir() if item.is_dir() and item.name])
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