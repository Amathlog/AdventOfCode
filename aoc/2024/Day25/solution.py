import copy
from typing import List, Tuple, Dict, Optional, Set
from aoc.common.parse_entry import parse_all
from aoc.common.utils import profile

entries, example_entries = parse_all(__file__, "entry.txt", "example.txt")

@profile
def part_one(entry: List[str]) -> int:
    keys = []
    locks = []
    for i in range((len(entry) + 1) // 8):
        start = 8*i
        end = 8*(i+1)-1
        lines = entry[start+1:end-1]
        is_lock = entry[start][0] == "#"

        columns = [0] * 5
        for line in lines:
            for j, c in enumerate(line):
                if c == "#":
                    columns[j] += 1

        if is_lock:
            locks.append(columns)
        else:
            keys.append(columns)

    count = 0
    for key in keys:
        for lock in locks:
            valid = True
            for i in range(5):
                if key[i] + lock[i] > 5:
                    valid = False
                    break
            if valid:
                count += 1
    return count


@profile
def part_two(entry: List[str]) -> int:
    return 0


if __name__ == "__main__":
    print("Part 1 example:", part_one(example_entries))
    print("Part 1 entry:", part_one(entries))

    print("Part 2 example:", part_two(example_entries))
    print("Part 2 entry:", part_two(entries))
