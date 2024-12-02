import copy
from typing import List, Tuple, Dict, Optional, Set
from aoc.common.parse_entry import parse_all
from aoc.common.utils import profile

entries, example_entries = parse_all(__file__, "entry.txt", "example.txt")

def analyze(line: List[int]) -> Tuple[bool, int]:
    diff = 0
    valid = True
    for i in range(len(line) - 1):
        new_diff = line[i+1] - line[i]
        if new_diff == 0 or abs(new_diff) > 3 or diff * new_diff < 0:
            valid = False
            break
        diff = new_diff

    return valid, i

@profile
def solve(entry: List[str], remove_bad_level: bool) -> int:
    data = [[int(c) for c in line.split()] for line in entry]
    result = 0
    for line in data:
        valid, i = analyze(line)

        if remove_bad_level and not valid:
            new_lines = [line[:i-1] + line[i:], line[:i] + line[i+1:], line[:i+1] + line[i+2:]]
            for new_line in new_lines:
                valid, _ = analyze(new_line)
                if valid:
                    break

        if valid:
            result += 1

    return result


if __name__ == "__main__":
    print("Part 1 example:", solve(example_entries, False))
    print("Part 1 entry:", solve(entries, False))

    print("Part 2 example:", solve(example_entries, True))
    print("Part 2 entry:", solve(entries, True))
