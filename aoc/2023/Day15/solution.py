import copy
from typing import List, Tuple, Dict, Optional, Set
from aoc.common.parse_entry import parse_all
from aoc.common.utils import profile

entries, example_entries = parse_all(__file__, "entry.txt", "example.txt")

class LabeledLens:
    def __init__(self, label: str, lens: int) -> None:
        self.label = label
        self.lens = lens

    def __eq__(self, other: "LabeledLens") -> bool:
        return self.label == other.label
    
    def __repr__(self) -> str:
        return f"{self.label} {self.lens}"

def HASH(e: str) -> int:
    res = 0
    for c in e:
        res += ord(c)
        res *= 17
        res %= 256
    return res

@profile
def part_one(entry: List[str]) -> int:
    return sum(map(HASH, entry[0].split(",")))

@profile
def part_two(entry: List[str]) -> int:
    boxes = [[] for _ in range(256)]
    for inst in entry[0].split(","):
        if inst[-1] == "-":
            labeled_lens = LabeledLens(inst[:-1], None)
        else:
            labeled_lens = LabeledLens(inst[:-2], int(inst[-1]))
        
        box = boxes[HASH(labeled_lens.label)]
        if labeled_lens.lens is None:
            try:
                box.remove(labeled_lens)
            except ValueError:
                pass
        else:
            try:
                index = box.index(labeled_lens)
                box[index] = labeled_lens
            except ValueError:
                box.append(labeled_lens)

    res = 0
    for i, box in enumerate(boxes):
        for j, labeled_lens in enumerate(box):
            res += (i+1) * (j+1) * labeled_lens.lens

    return res


if __name__ == "__main__":
    print("Part 1 example:", part_one(example_entries))
    print("Part 1 entry:", part_one(entries))

    print("Part 2 example:", part_two(example_entries))
    print("Part 2 entry:", part_two(entries))
