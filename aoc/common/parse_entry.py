from typing import List
import os
from pathlib import Path

default_separator = "---"

def parse_entry_multiple_parts(path: str, separator: str, expected_parts: int) -> List[List[str]]:
    with path.open("r") as f:
        entries = f.readlines()

    if len(entries) == 0:
        return [None] * expected_parts

    indexes = [-1]
    for i in range(len(entries)):
        entries[i] = entries[i].strip()
        if entries[i] == separator:
            indexes.append(i)

    if entries[-1] != separator:
        indexes.append(len(entries))

    result = [entries[indexes[i]+1:indexes[i+1]] for i in range(len(indexes) - 1)]
    while len(result) < expected_parts:
        result.append(None)
    
    assert len(result) == expected_parts
    return result

def parse_entry(path: str) -> List[str]:
    with path.open("r") as f:
        entries = f.readlines()

    for i in range(len(entries)):
        entries[i] = entries[i].strip()

    return entries


def parse_all(relative_file: str, *args: str) -> List[str]:
    root = Path(os.path.abspath(relative_file)).parent

    return [parse_entry(root / file) for file in args]

def parse_all_multiple_parts(relative_file: str, separator: str, expected_parts: int, *args: str) -> List[str]:
    root = Path(os.path.abspath(relative_file)).parent

    return [parse_entry_multiple_parts(root / file, separator, expected_parts) for file in args]
