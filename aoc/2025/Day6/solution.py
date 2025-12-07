import copy
from typing import List, Tuple, Dict, Optional, Set
from aoc.common.parse_entry import parse_all
from aoc.common.utils import profile
import re

entries, example_entries = parse_all(__file__, "entry.txt", "example.txt", should_strip=False)

@profile
def part_one(entry: List[str]) -> int:
    regex_digits = re.compile(r" *(\d+) *")
    regex_ops = re.compile(r" *([\+\*]) *")

    lines = [[int(i) for i in regex_digits.findall(e)] for e in entry[:-1]]
    ops = regex_ops.findall(entry[-1])

    result = 0
    for i in range(len(lines[0])):
        temp = lines[0][i]
        for l in lines[1:]:
            if ops[i] == "+":
                temp += l[i]
            else:
                temp *= l[i]
        result += temp

    return result

@profile
def part_two(entry: List[str]) -> int:
    regex_ops = re.compile(r" *([\+\*]) *")
    ops = regex_ops.findall(entry[-1])

    result = 0
    curr_op_idx = len(ops) - 1

    temp = None
    for i in reversed(range(len(entry[0])-1)):
        column = "".join((e[i] for e in entry[:-1]))
        column = column.replace(" ", "")

        if len(column) != 0:
            num = int(column)
            if temp is None:
                temp = num
            elif ops[curr_op_idx] == "+":
                temp += num
            else:
                temp *= num

        if len(column) == 0 or i == 0:
            result += temp
            temp = None
            curr_op_idx -= 1
            continue

    return result


if __name__ == "__main__":
    print("Part 1 example:", part_one(example_entries))
    print("Part 1 entry:", part_one(entries))

    print("Part 2 example:", part_two(example_entries))
    print("Part 2 entry:", part_two(entries))
