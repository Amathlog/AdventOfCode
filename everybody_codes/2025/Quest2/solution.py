import copy
from typing import List, Tuple, Dict, Optional, Set
from aoc.common.parse_entry import parse_all_multiple_parts, default_separator
from aoc.common.utils import profile
from aoc.common.point import Vector
import math

entries, example_entries = parse_all_multiple_parts(__file__, default_separator, 3, "entry.txt", "example.txt")

class Complex:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __mul__(self, other) -> "Complex":
        return Complex(self.x * other.x - self.y * other.y, self.x * other.y + self.y * other.x)
    
    def __floordiv__(self, other) -> "Complex":
        res = Complex(self.x / other.x, self.y / other.y)
        res.x = int(math.floor(res.x) if res.x >= 0 else math.ceil(res.x))
        res.y = int(math.floor(res.y) if res.y >= 0 else math.ceil(res.y))
        
        return res
    
    def __add__(self, other) -> "Complex":
        return Complex(self.x + other.x, self.y + other.y)
    
    def __repr__(self):
        return f"[{self.x}, {self.y}]"

@profile
def part_one(entry: List[str]) -> int:
    entry_split = entry[0][3:-1].split(',')
    a = Complex(int(entry_split[0]), int(entry_split[1]))
    constant = Complex(10, 10)
    r = Complex(0, 0)

    for i in range(3):
        r = ((r * r) // constant) + a

    return r

@profile
def part_two(entry: List[str]) -> int:
    entry_split = entry[0][3:-1].split(',')
    a = Complex(int(entry_split[0]), int(entry_split[1]))
    constant = Complex(100000, 100000)
    res = []

    def run(curr: Complex) -> bool:
        r = Complex(0, 0)
        for i in range(100):
            r = ((r * r) // constant) + curr
            if abs(r.x) > 1000000 or abs(r.y) > 1000000:
                return False
        
        return True
    
    count = 0
    for i in range(101):
        res.append([])
        for j in range(101):
            r = run(a + Complex(j * 10, i * 10))
            res[-1].append(r)
            if r:
                count += 1

    # Print figure:
    # p = ""
    # for line in res:
    #     for r in line:
    #         p += 'x' if r else '·'
    #     p += '\n'
    # print(p)

    return count

@profile
def part_three(entry: List[str]) -> int:
    entry_split = entry[0][3:-1].split(',')
    a = Complex(int(entry_split[0]), int(entry_split[1]))
    constant = Complex(100000, 100000)
    res = []

    def run(curr: Complex) -> bool:
        r = Complex(0, 0)
        for i in range(100):
            r = ((r * r) // constant) + curr
            if abs(r.x) > 1000000 or abs(r.y) > 1000000:
                return False
        
        return True
    
    count = 0
    for i in range(1001):
        res.append([])
        for j in range(1001):
            r = run(a + Complex(j, i))
            res[-1].append(r)
            if r:
                count += 1

    # Print figure:
    # p = ""
    # for line in res:
    #     for r in line:
    #         p += 'x' if r else '·'
    #     p += '\n'
    # print(p)

    return count


if __name__ == "__main__":
    print("Part 1 example:", part_one(example_entries[0]))
    print("Part 1 entry:", part_one(entries[0]))

    print("Part 2 example:", part_two(example_entries[1]))
    print("Part 2 entry:", part_two(entries[1]))

    print("Part 3 example:", part_three(example_entries[2]))
    print("Part 3 entry:", part_three(entries[2]))
