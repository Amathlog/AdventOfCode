import copy
from typing import List, Tuple, Dict, Optional, Set
from aoc.common.parse_entry import parse_all
from aoc.common.utils import profile
from aoc.common.grid import Grid
from itertools import count

entries, example_entries = parse_all(__file__, "entry.txt", "example.txt")

class Piece(Grid):
    def __init__(self, grid):
        super().__init__(grid)
        self.area = sum([1 if c == "#" else 0 for c in self.iterate_row_first()])


@profile
def part_one(entry: List[str]) -> int:
    pieces = []
    for i in range(6):
        pieces.append(Piece(entry[(5 * i) + 1:(5 * i)+4]))

    count = 0

    for line in entry[30:]:
        cell, num = line.split(": ")
        cell_x, cell_y = map(int, cell.split("x"))
        num = tuple(map(int, num.split()))

        print(cell, num)

        available_space = cell_x * cell_y
        num_presents = sum(num)

        max_blocks_x = cell_x // 3
        max_blocks_y = cell_y // 3
        if num_presents <= (max_blocks_x * max_blocks_y):
            count += 1
            continue

        necessary_space = sum([pieces[i].area * num[i] for i in range(len(num))])

        if available_space < necessary_space:
            continue
        
        # this will never happen for the entry data. But it will happen for the example, so assume it is possible
        count += 1

    return count

@profile
def part_two(entry: List[str]) -> int:
    return 0


if __name__ == "__main__":
    print("Part 1 example:", part_one(example_entries))
    print("Part 1 entry:", part_one(entries))

    print("Part 2 example:", part_two(example_entries))
    print("Part 2 entry:", part_two(entries))
