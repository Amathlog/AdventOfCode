from pathlib import Path
import os
import copy
from typing import List, Tuple, Dict
from aoc.common.parse_entry import parse_all

entries, example_entries = parse_all(__file__, "entry.txt", "example.txt")


def part_one_and_two(entry: List[str]) -> int:
    res = [0, 0]
    for e in entry:
        values = list(map(int, e.split()))
        sequence = [values]
        while True and len(sequence[-1]) > 0:
            diff = [sequence[-1][i+1] - sequence[-1][i] for i in range(len(sequence[-1]) - 1)]
            if all((v == 0 for v in diff)):
                break
            sequence.append(diff)

        assert(len(sequence[-1]) > 0)

        temp_last = 0
        temp_first = 0
        for s in reversed(sequence):
            temp_last += s[-1]
            temp_first = s[0] - temp_first
        
        res[0] += temp_last
        res[1] += temp_first
    
    return res


if __name__ == "__main__":
    print("Part 1 and 2 example:", part_one_and_two(example_entries))
    print("Part 1 and 2 entry:", part_one_and_two(entries))
