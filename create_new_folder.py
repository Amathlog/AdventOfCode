from pathlib import Path
import sys
import os
import urllib.request

year_number = sys.argv[1]
day_number = sys.argv[2]

template = """from pathlib import Path
import os

entry_file = Path(os.path.abspath(__file__)).parent / "entry.txt"

with entry_file.open("r") as f:
    entries = f.readlines()
"""

folder = Path(os.path.abspath(__file__)).parent

year = folder / year_number
day = year / ("Day" + day_number)
entry = day / "entry.txt"
solution = day / "solution.py"

day.mkdir(parents=True, exist_ok=True)

with solution.open('w') as f:
    f.write(template)

entry.touch()
