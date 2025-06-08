import copy
from typing import List, Tuple, Dict, Optional, Set, Generator
from aoc.common.parse_entry import parse_all
from aoc.common.utils import profile
from collections import defaultdict
import re

entries, example_entries, example2_entries = parse_all(__file__, "entry.txt", "example.txt", "example2.txt")

class Mask:
    def __init__(self, mask: str, init_perm: bool = False):
        self.mask = mask
        self.ones = 0
        self.zeros = 0
        self.permutations = []
        for i, c in enumerate(mask):
            bit_one = 1 if c == '1' else 0
            bit_zero = 0 if c == '0' else 1
            self.ones = (self.ones << 1) + bit_one
            self.zeros = (self.zeros << 1) + bit_zero
            if c == "X" and init_perm:
                new_permutations = []
                mask = 2**(35-i)
                inv_mask = ~mask
                if len(self.permutations) == 0:
                    self.permutations = [(mask, 2**36-1), (0, inv_mask)]
                else:
                    for one, zero in self.permutations:
                        new_permutations.append((one | mask, zero))
                        new_permutations.append((one, zero & inv_mask))
                    self.permutations.extend(new_permutations)

    def apply(self, v: int) -> int:
        return (v | self.ones) & self.zeros
    
    def apply_address_gen(self, addr: int) -> Generator:
        for one, zero in self.permutations:
            yield ((addr | one) & zero) | self.ones


@profile
def part_one(entry: List[str]) -> int:
    mem = defaultdict(int)
    mask_regex = re.compile("mask = (.*)")
    mem_regex = re.compile("mem\[(\d+)\] = (\d+)")
    i = 0
    curr_mask = None
    for line in entry:
        mask_res = mask_regex.findall(line)
        if len(mask_res) > 0:
            curr_mask = Mask(mask_res[0])
            continue

        assert(curr_mask is not None)
        pos, value = mem_regex.findall(line)[0]
        value = curr_mask.apply(int(value))
        mem[pos] = value

    return sum(mem.values())
        

@profile
def part_two(entry: List[str]) -> int:
    mem = defaultdict(int)
    mask_regex = re.compile("mask = (.*)")
    mem_regex = re.compile("mem\[(\d+)\] = (\d+)")
    i = 0
    curr_mask = None
    for line in entry:
        mask_res = mask_regex.findall(line)
        if len(mask_res) > 0:
            curr_mask = Mask(mask_res[0], True)
            continue

        assert(curr_mask is not None)
        pos, value = mem_regex.findall(line)[0]
        for new_pos in curr_mask.apply_address_gen(int(pos)):
            mem[new_pos] = int(value)

    return sum(mem.values())


if __name__ == "__main__":
    print("Part 1 example:", part_one(example_entries))
    print("Part 1 entry:", part_one(entries))

    print("Part 2 example:", part_two(example2_entries))
    print("Part 2 entry:", part_two(entries))
