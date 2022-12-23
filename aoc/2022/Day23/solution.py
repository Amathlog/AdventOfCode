from pathlib import Path
import os
import copy
from typing import List, Tuple, Dict
from collections import namedtuple
from enum import Enum

entry_file = Path(os.path.abspath(__file__)).parent / "entry.txt"
example_file = Path(os.path.abspath(__file__)).parent / "example.txt"

def parse_entry(path: str) -> List[str]:
    with path.open("r") as f:
        entries = f.readlines()

    for i in range(len(entries)):
        if entries[i][-1] == '\n':
            entries[i] = entries[i][:-1]

    return entries

entries = parse_entry(entry_file)
example_entries = parse_entry(example_file)


class Direction(Enum):
    N = 0
    NE = 1
    E = 2
    SE = 3
    S = 4
    SW = 5
    W = 6
    NW = 7

def get_incr(dir: Direction) -> "Point":
    if dir == Direction.N:
        return Point(0, -1)
    if dir == Direction.E:
        return Point(1, 0)
    if dir == Direction.S:
        return Point(0, 1)
    return Point(-1, 0)


class Point:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __add__(self, other: "Point") -> "Point":
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other: "Point") -> "Point":
        return Point(self.x - other.x, self.y - other.y)

    def __mul__(self, other: int) -> "Point":
        return Point(self.x * other, self.y * other)

    def distance(self, other: "Point") -> int:
        dist = self - other
        return abs(dist.x) + abs(dist.y)

    def __repr__(self) -> str:
        return f"({self.x}, {self.y})"

    def __eq__(self, other: "Point") -> bool:
        return self.x == other.x and self.y == other.y
    
    def __hash__(self) -> int:
        return hash((self.x, self.y))

class Elf:
    def __init__(self, initial_pos: "Point"):
        self.pos = initial_pos
        self.others: List[bool] = [False] * 8
        self.old_pos = self.pos

    def reset_others(self):
        self.others = [False] * 8

    def scan_others(self, all_pos: set[Point]):
        for i, incr in enumerate([Point(0, -1), Point(1, -1), Point(1, 0), Point(1, 1), Point(0, 1), Point(-1, 1), Point(-1, 0), Point(-1, -1)]):
            self.others[i] = (self.pos + incr) in all_pos

    @property
    def should_move(self):
        return any(self.others)

    def tentative_move(self, dir_order: List[Direction]) -> bool:
        self.old_pos = self.pos
        if not self.should_move:
            return False
        for dir in dir_order:
            can_move = True
            for i in [(dir.value - 1) % 8, dir.value, dir.value + 1]:
                if self.others[i]:
                    can_move = False
                    break
            
            if can_move:
                self.pos = self.pos + get_incr(dir)
                return True

        return False

    def backtrack(self):
        self.pos = self.old_pos


def print_elves(map_pos_elves: Dict[Point, List[Elf]]):
    min_x = min((p.x for p in map_pos_elves.keys()))
    max_x = max((p.x for p in map_pos_elves.keys()))
    min_y = min((p.y for p in map_pos_elves.keys()))
    max_y = max((p.y for p in map_pos_elves.keys()))

    res = ""
    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            res += "#" if Point(x, y) in map_pos_elves else "."
        res += "\n"
    print(res)

def count_empty(map_pos_elves: Dict[Point, List[Elf]]):
    min_x = min((p.x for p in map_pos_elves.keys()))
    max_x = max((p.x for p in map_pos_elves.keys()))
    min_y = min((p.y for p in map_pos_elves.keys()))
    max_y = max((p.y for p in map_pos_elves.keys()))

    res = 0
    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            if Point(x, y) not in map_pos_elves:
                res += 1
    return res


def solve(entries: List[str]):
    all_elves: List[Elf] = []
    map_pos_elves: Dict[Point, List[Elf]] = {}

    for y in range(len(entries)):
        for x in range(len(entries[0])):
            if entries[y][x] == "#":
                all_elves.append(Elf(Point(x, y)))
                map_pos_elves[all_elves[-1].pos] = [all_elves[-1]]

    directions = [Direction.N, Direction.S, Direction.W, Direction.E]

    #print_elves(map_pos_elves)

    i = 0
    while True:
        if i == 10:
            print("Part 1: Number of empty tiles =", count_empty(map_pos_elves))

        temp_map_pos = {}
        problematic_positions = set()
        for elf in all_elves:
            elf.reset_others()
            elf.scan_others(map_pos_elves)
            elf.tentative_move(directions)
            new_pos = elf.pos
            if new_pos not in temp_map_pos:
                temp_map_pos[new_pos] = [elf]
            else:
                temp_map_pos[new_pos].append(elf)
                problematic_positions.add(new_pos)

        for pos in problematic_positions:
            for elf in temp_map_pos[pos]:
                elf.backtrack()
                assert elf.pos not in temp_map_pos
                temp_map_pos[elf.pos] = [elf]
            del temp_map_pos[pos]
        
        # Stopped moving
        if temp_map_pos.keys() == map_pos_elves.keys():
            break

        map_pos_elves = temp_map_pos

        directions = directions[1:] + [directions[0]]
        i += 1
        #print_elves(map_pos_elves)

    print("Part 2: Nb rounds to finish the process =", i + 1)

if __name__ == "__main__":
    print("For example")
    solve(example_entries)

    print("For my entry")
    solve(entries)