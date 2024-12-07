from typing import List, Tuple
from aoc.common.parse_entry import parse_all
from aoc.common.utils import profile
from aoc.common.multithread import MultiWrapper, execute_async

entries, example_entries = parse_all(__file__, "entry.txt", "example.txt")

def concat(left: int, right: int) -> int:
    return int(str(left) + str(right))

def recurse(left: int, right: List[int], curr: int, use_concat: bool) -> bool:
    if len(right) == 0:
        return left == curr
    
    temp = curr * right[0]
    if temp <= left and recurse(left, right[1:], temp, use_concat):
        return True
    
    temp = curr + right[0]
    if temp <= left and recurse(left, right[1:], temp, use_concat):
        return True
    
    if use_concat:
        temp = concat(curr, right[0])
        if temp <= left and recurse(left, right[1:], temp, use_concat):
            return True
    
    return False

@profile
def solve(entry: List[str]) -> int:
    result_part1 = 0
    result_part2 = 0

    for e in entry:
        left, right = e.split(": ")
        left = int(left)
        right = [int(r) for r in right.split()]
        if recurse(left, right[1:], right[0], False):
            result_part1 += left
            result_part2 += left
        elif recurse(left, right[1:], right[0], True):
            result_part2 += left

    return result_part1, result_part2


def get_result(left: int, right: List[int]) -> Tuple[int, int]:
    if recurse(left, right[1:], right[0], False):
        return (left, left)
    elif recurse(left, right[1:], right[0], True):
        return (0, left)
    else:
        return (0, 0)

def reduce(values: List[Tuple[int]]):
    res_1 = 0
    res_2 = 0
    for a, b in values:
        res_1 += a
        res_2 += b
    return (res_1, res_2)

@profile
def solve_async(entry: List[str]) -> int:
    result_part1 = 0
    result_part2 = 0

    input = []

    for e in entry:
        left, right = e.split(": ")
        left = int(left)
        right = [int(r) for r in right.split()]
        input.append((left, right))

    return execute_async(16, MultiWrapper(get_result), input, reduce)


if __name__ == "__main__":
    print("Part 1 and 2 example:", solve(example_entries))
    print("Part 1 and 2 entry:", solve_async(entries))
