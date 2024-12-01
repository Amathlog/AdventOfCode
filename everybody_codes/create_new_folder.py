from pathlib import Path
import sys
import os

template = """import copy
from typing import List, Tuple, Dict, Optional, Set
from aoc.common.parse_entry import parse_all_multiple_parts, default_separator
from aoc.common.utils import profile

entries, example_entries = parse_all_multiple_parts(__file__, default_separator, 3, "entry.txt", "example.txt")

@profile
def part_one(entry: List[str]) -> int:
    return 0

@profile
def part_two(entry: List[str]) -> int:
    return 0

@profile
def part_three(entry: List[str]) -> int:
    return 0


if __name__ == "__main__":
    print("Part 1 example:", part_one(example_entries[0]))
    print("Part 1 entry:", part_one(entries[0]))

    print("Part 2 example:", part_two(example_entries[1]))
    print("Part 2 entry:", part_two(entries[1]))

    print("Part 3 example:", part_three(example_entries[2]))
    print("Part 3 entry:", part_three(entries[2]))
"""

folder = Path(os.path.abspath(__file__)).parent

if len(sys.argv) < 3:
    year_number = max([item.name for item in folder.iterdir() if item.is_dir()])
    year = folder / year_number
    day = max([int(item.name[5:]) for item in year.iterdir() if item.is_dir()])
    day_number = str(day + 1)
    pass
else:
    year_number = sys.argv[1]
    year = folder / year_number
    day_number = sys.argv[2]

day = year / ("Quest" + day_number)
entry = day / "entry.txt"
example = day / "example.txt"
solution = day / "solution.py"

day.mkdir(parents=True, exist_ok=True)

with solution.open('w') as f:
    f.write(template)

entry.touch()
example.touch()