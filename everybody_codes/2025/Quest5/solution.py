import copy
from typing import List, Tuple, Dict, Optional, Set
from aoc.common.parse_entry import parse_all_multiple_parts, default_separator
from aoc.common.utils import profile

entries, example_entries = parse_all_multiple_parts(__file__, default_separator, 3, "entry.txt", "example.txt")

class Segment:
    def __init__(self, middle: int):
        self.middle = middle
        self.left = None
        self.right = None

    def try_placement(self, value: int) -> bool:
        if self.left is None and value < self.middle:
            self.left = value
            return True
        
        if self.right is None and value > self.middle:
            self.right = value
            return True
        
        return False
    
    def number(self):
        r = ""
        if self.left is not None:
            r += str(self.left)
        r += str(self.middle)
        if self.right is not None:
            r += str(self.right)

        return int(r)
    
    def __repr__(self):
        left = f"{self.left:2d} -" if self.left is not None else "    "
        right = f" - {self.right:2d}" if self.right is not None else ""
        return left + f" {self.middle:2d}" + right

class Sword:
    def __init__(self, id: int):
        self.id = id
        self.segments: List[Segment] = []

    @staticmethod
    def construct(e: str) -> "Sword":
        id, rest = e.split(":")
        sword = Sword(int(id))
        for v in rest.split(","):
            placed = False
            v = int(v)
            for seg in sword.segments:
                if seg.try_placement(v):
                    placed = True
                    break

            if not placed:
                sword.segments.append(Segment(v))
        
        return sword
    
    def quality(self) -> int:
        return int("".join([str(s.middle) for s in self.segments]))
    
    def __repr__(self):
        if len(self.segments) == 0:
            return ""
        
        r = str(self.segments[0])
        for s in self.segments[1:]:
            r += "\n      |\n"
            r += str(s)

        return r
    
    def __lt__(self, other: "Sword"):
        self_quality = self.quality()
        other_quality = other.quality()
        if self_quality != other_quality:
            return self_quality < other_quality
        
        for i in range(min(len(self.segments), len(other.segments))):
            self_number = self.segments[i].number()
            other_number = other.segments[i].number()
            if self_number != other_number:
                return self_number < other_number
            
        if len(self.segments) != len(other.segments):
            return len(self.segments) < len(other.segments)
        
        return self.id < other.id


@profile
def part_one(entry: List[str]) -> int:
    sword = Sword.construct(entry[0])
    return sword.quality()


@profile
def part_two(entry: List[str]) -> int:
    swords = sorted([Sword.construct(e) for e in entry], key=lambda s: s.quality())
    return swords[-1].quality() - swords[0].quality()

@profile
def part_three(entry: List[str]) -> int:
    swords = sorted([Sword.construct(e) for e in entry], reverse=True)
    res = 0
    for i, s in enumerate(swords):
        res += (i+1) * s.id

    return res


if __name__ == "__main__":
    print("Part 1 example:", part_one(example_entries[0]))
    print("Part 1 entry:", part_one(entries[0]))

    print("Part 2 example:", part_two(example_entries[1]))
    print("Part 2 entry:", part_two(entries[1]))

    print("Part 3 example:", part_three(example_entries[2]))
    print("Part 3 entry:", part_three(entries[2]))
