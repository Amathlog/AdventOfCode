import copy
from typing import List, Tuple, Dict, Optional, Set
from aoc.common.parse_entry import parse_all
from aoc.common.utils import profile

entries, example_entries = parse_all(__file__, "entry.txt", "example.txt")

def is_cycle(seq: List[int]) -> bool:
    for middle in range(1, (len(seq) // 2 + 1)):
        valid = True
        for i in range(middle):
            if seq[-i-1] != seq[-i-1-middle]:
                valid = False
                break
        
        if valid:
            return True, middle

    return False, None

@profile
def part(entry: List[str], num: int) -> int:
    res = []
    for line in entry:
        e = line.split(',')
        all_numbers = {}
        last_spoken = None
        spoken = 0
        for i in range(num):
            if i < len(e):
                spoken = int(e[i])
            else:
                if last_spoken not in all_numbers:
                    spoken = 0
                else:
                    spoken = i - all_numbers[last_spoken]

            all_numbers[last_spoken] = i
            last_spoken = spoken
                
        res.append(last_spoken)
        break
    return res[0]


if __name__ == "__main__":
    print("Part 1 example:", part(example_entries, 2020))
    print("Part 1 entry:", part(entries, 2020))

    print("Part 2 example:", part(example_entries, 30000000))
    print("Part 2 entry:", part(entries, 30000000))
