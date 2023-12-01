from typing import List

def parse_entry(path: str) -> List[str]:
    with path.open("r") as f:
        entries = f.readlines()

    for i in range(len(entries)):
        if entries[i][-1] == '\\n':
            entries[i] = entries[i][:-1]

    return entries
