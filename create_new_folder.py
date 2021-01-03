from pathlib import Path
import sys
import os

folder = Path(os.path.abspath(__file__)).parent

year = folder / sys.argv[1]
day = year / ("Day" + sys.argv[2])
entry = day / "entry.txt"
solution = day / "solution.py"

day.mkdir(parents=True, exist_ok=True)
entry.touch()
solution.touch()