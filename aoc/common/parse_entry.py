from typing import List
import os
from pathlib import Path


def parse_entry(path: str) -> List[str]:
    with path.open("r") as f:
        entries = f.readlines()

    for i in range(len(entries)):
        entries[i] = entries[i].strip()

    return entries


def parse_all(relative_file: str, *args: str) -> List[str]:
    root = Path(os.path.abspath(relative_file)).parent

    return [parse_entry(root / file) for file in args]
