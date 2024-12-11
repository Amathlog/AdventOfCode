import copy
from typing import List, Tuple, Dict, Optional, Set
from aoc.common.parse_entry import parse_all
from aoc.common.utils import profile
from collections import defaultdict

entries, example_entries = parse_all(__file__, "entry.txt", "example.txt")

@profile
def solve(entry: List[str]) -> int:
    stones = defaultdict(int)
    for s in entry[0].split():
        num = int(s)
        stones[num] += 1

    mid_results = 0

    for i in range(75):
        if i == 25:
            mid_results = sum(stones.values())

        new_stones = defaultdict(int)
        for k in stones.keys():
            count = stones[k]

            if k == 0:
                new_stones[1] += count
                continue

            num = str(k)
            if (len(num) & 1) == 0:
                mid = len(num)//2
                new_stones[int(num[:mid])] += count
                new_stones[int(num[mid:])] += count
            else:
                new_stones[k * 2024] += count

        stones = new_stones

    return mid_results, sum(stones.values())

if __name__ == "__main__":
    print("Part 1 and 2 example:", solve(example_entries))
    print("Part 1 and 2 entry:", solve(entries))
