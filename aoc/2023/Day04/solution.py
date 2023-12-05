from pathlib import Path
import os
import copy
from typing import List, Tuple, Dict
from aoc.common.parse_entry import parse_all

entries, example_entries = parse_all(__file__, "entry.txt", "example.txt")


def get_score(entry: List[str]) -> List[int]:
    res = []
    for row in entry:
        _, rest = row.split(": ")
        winning_numbers, numbers = rest.split(" | ")
        winning_numbers = set([int(x) for x in winning_numbers.split()])
        numbers = set([int(x) for x in numbers.split()])

        wins = numbers.intersection(winning_numbers)
        res.append(len(wins))
    
    return res


def part_one(scores: List[int]) -> int:
    res = 0
    for score in scores:
        if score == 0:
            continue

        res += 2 ** (score - 1)
    return res


def part_two(scores: List[int]) -> int:
    copies = [1] * len(scores)

    for i, score in enumerate(scores):
        if score == 0:
            continue

        for x in range(score):
            idx = i + x + 1
            if idx >= len(scores):
                break
            copies[idx] += copies[i]
    
    return sum(copies)


if __name__ == "__main__":
    example_scores = get_score(example_entries)
    entry_scores = get_score(entries)

    print("Part 1 example: ", part_one(example_scores))
    print("Part 1 entry: ", part_one(entry_scores))

    print("Part 2 example: ", part_two(example_scores))
    print("Part 2 entry: ", part_two(entry_scores))
