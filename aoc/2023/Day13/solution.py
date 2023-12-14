from pathlib import Path
import os
import copy
from typing import List, Tuple, Dict, Optional
from aoc.common.parse_entry import parse_all
import math

entries, example_entries = parse_all(__file__, "entry.txt", "example.txt")

def convert_to_bitfield(e: str) -> int:
    res = 0
    for c in e:
        res = (res << 1) + (1 if c == "#" else 0)
    return res

def count_bits(value: int) -> int:
    res = 0
    while value > 0:
        if (value & 1) == 1:
            res += 1
        value >>= 1
    return res 

# Return the row with a perfect fold (None if it doesn't exist) and the row with an almsot perfect fold (1 difference, None if it doesn't exist)
def summarize(note: List[int]) -> Tuple[Optional[int], Optional[int]]:
    perfect_fold = None
    almost_perfect_fold = None
    for i in range(0, len(note) - 1):
        end = min(2 * i + 1, len(note) - 1)
        start = max(2 * (i+1) - len(note), 0)
        diff = 0
        while start < end and diff <= 1:
            diff += count_bits(note[start] ^ note[end])
            start += 1
            end -= 1

        if diff == 0:
            perfect_fold = i + 1
        elif diff == 1:
            almost_perfect_fold = i + 1
        
        if perfect_fold is not None and almost_perfect_fold is not None:
            break
    
    return perfect_fold, almost_perfect_fold


def part_one_and_two(entry: List[str]) -> int:
    perfect_fold = 0
    almost_perfect_fold = 0
    note_indices = [-1] + [i for i, e in enumerate(entry) if len(e) == 0] + [len(entry)]

    for i in range(len(note_indices) - 1):
        start = note_indices[i] + 1
        end = note_indices[i+1]
        note_str = entry[start:end]
        note = list(map(convert_to_bitfield, note_str))

        row_perfect_fold, row_almost_perfect_fold = summarize(note)
        if row_perfect_fold is not None:
            perfect_fold += row_perfect_fold * 100
        if row_almost_perfect_fold is not None:
            almost_perfect_fold += row_almost_perfect_fold * 100

        if row_perfect_fold is None or row_almost_perfect_fold is None:
            reversed_note = list(map(convert_to_bitfield, ["".join([e[j] for e in note_str]) for j in range(len(note_str[0]))]))

            col_perfect_fold, col_almost_perfect_fold = summarize(reversed_note)
            assert(col_perfect_fold is not None or col_almost_perfect_fold is not None)
            if col_perfect_fold is not None:
                perfect_fold += col_perfect_fold
            if col_almost_perfect_fold is not None:
                almost_perfect_fold += col_almost_perfect_fold

    return perfect_fold, almost_perfect_fold


if __name__ == "__main__":
    print("Part 1 and 2 example:", part_one_and_two(example_entries))
    print("Part 1 and 2 entry:", part_one_and_two(entries))

