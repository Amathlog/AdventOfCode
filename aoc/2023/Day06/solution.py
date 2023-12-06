from pathlib import Path
import os
import copy
import math
from typing import List, Tuple, Dict
from aoc.common.parse_entry import parse_all

entries, example_entries = parse_all(__file__, "entry.txt", "example.txt")

# With x being the time spent pressing the button
# distance = (time - t) * t
# To find the time we have to press the button to reach the record, we solve this quadratic function
# -t**2 + time * t - record = 0 which have 2 roots, t_1 and t_2. So we beat the record if we press the button longer than
# [t_1, t_2] (t_1 and t_2 excluded, because it would mean we would reach the record, not beat it).
# so if t_1 and t_2 are integers, we increment/decrement by 1 respectively, otherwise, we take the ceil/floor respectively.
# Of course we can't press the button longer than the race time, so t_2 can be at most "time".
# And finally the number of possibilities are t_2 - t_1 + 1 
def compute(time: int, distance: int) -> int:
    record_t_1 = (time - math.sqrt(time**2 - 4 * distance)) / 2
    record_t_2 = (time + math.sqrt(time**2 - 4 * distance)) / 2

    t_1 = math.ceil(record_t_1)
    if t_1 == record_t_1:
        t_1 += 1
    t_2 = math.floor(record_t_2)
    if t_2 == record_t_2:
        t_2 -= 1

    t_2 = min(t_2, time)

    return (t_2 - t_1 + 1)


def part_one(entry: List[str]) -> int:
    all_time = map(int, entry[0].split()[1:])
    all_distance = map(int, entry[1].split()[1:])

    res = 1

    for time, distance in zip(all_time, all_distance):
        res *= compute(time, distance)

    return res

def part_two(entry: List[str]) -> int:
    # Remove all spaces and reconstruct the int.
    time = int("".join(entry[0].split()[1:]))
    distance = int("".join(entry[1].split()[1:]))

    return compute(time, distance)


if __name__ == "__main__":
    print("Part 1 example:", part_one(example_entries))
    print("Part 1 entry:", part_one(entries))

    print("Part 2 example:", part_two(example_entries))
    print("Part 2 entry:", part_two(entries))
