import copy
from typing import List, Tuple, Dict, Optional, Set
from aoc.common.parse_entry import parse_all
from aoc.common.utils import profile

entries, example_entries = parse_all(__file__, "entry.txt", "example.txt")

@profile
def solve(entry: List[str]) -> int:
    order_less = {}
    order_greater = {}
    updates = []
    should_read_update = False
    for e in entry:
        if not should_read_update:
            if e == "":
                should_read_update = True
                continue

            a,b = e.split("|")
            a = int(a)
            b = int(b)
            if a not in order_less:
                order_less[a] = set()
            order_less[a].add(b)
            if b not in order_greater:
                order_greater[b] = set()
            order_greater[b].add(a)
        else:
            updates.append([int(c) for c in e.split(",")])

    class custom_int(int):
        def __init__(self, v):
            self.v = v

        def __lt__(a: int, b: int) -> bool:
            return a not in order_less or b not in order_less[a]

    valid_count = 0
    invalid_count = 0
    for update in updates:
        valid = True
        for i, number in enumerate(update[:-1]):
            if number not in order_less:
                valid = False
                break
            
            for other in update[i+1:]:
                if other not in order_less[number]:
                    valid = False
                    break
            if not valid:
                break
        
        if valid:
            valid_count += update[len(update) // 2]
        else:
            temp = sorted([custom_int(v) for v in update])
            invalid_count += temp[len(temp) // 2]

    return valid_count, invalid_count


if __name__ == "__main__":
    print("Part 1 and 2 example:", solve(example_entries))
    print("Part 1 and 2 entry:", solve(entries))