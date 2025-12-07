import copy
from typing import List, Tuple, Dict, Optional, Set
from aoc.common.parse_entry import parse_all
from aoc.common.utils import profile
from enum import IntEnum
import math

entries, example_entries = parse_all(__file__, "entry.txt", "example.txt")


class Direction(IntEnum):
    UP = 0,
    RIGHT = 1,
    DOWN = 2,
    LEFT = 3


class Tile:
    def __init__(self, input: List[str]):
        self.id = int(input[0][5:9])

        self.size = len(input[1])
        self.data = [[True if c == "#" else False for c in l] for l in input[1:]]
        self.rotation = 0
        self.flipped = False

    def __hash__(self):
        return hash((self.id, self.rotation, self.flipped))
    
    def __eq__(self, value):
        return value.id == self.id and value.rotation == self.rotation and value.flipped == self.flipped
    
    def reset(self):
        self.rotation = 0
        self.flipped = False

    def iterate(self, dir: Direction):
        real_dir = (dir + self.rotation) % 4
        # If left or right and flipped, left becomes right and vice versaList[List[Optional[Tile]]]
        if (real_dir % 2) == 1 and self.flipped:
            real_dir = (real_dir + 2) % 4

        if real_dir == Direction.UP or real_dir == Direction.DOWN:
            x = 0 if real_dir == Direction.UP else self.size - 1
            if self.flipped:
                return self.data[x][::-1]
            else:
                return self.data[x]
        else:
            y = 0 if real_dir == Direction.LEFT else self.size - 1
            return (self.data[x][y] for x in range(self.size))
        
    def match(self, self_dir: Direction, other:"Tile", other_dir: Direction):
        return all((x == y for (x, y) in zip(self.iterate(self_dir), other.iterate(other_dir))))
    
def backtrack(remaining_tiles: List[Tile], setup: List[List[Optional[Tile]]]) -> Optional[List[List[Optional[Tile]]]]:
    if len(remaining_tiles) == 0:
        return setup
    
    for i in range(len(setup)):
        for j in range(len(setup[i])):
            if setup[i][j] is not None:
                continue

            directions_to_test = []
            if i > 0:
                directions_to_test.append((Direction.UP, i - 1, j))
            if j > 0:
                directions_to_test.append((Direction.LEFT, i, j - 1))

            for tile in remaining_tiles:
                new_remaining_tiles = [t for t in remaining_tiles if t != tile]
                tile.reset()
                for rot in range(4):
                    tile.rotation = rot
                    for flipped in [False, True]:
                        tile.flipped = flipped
                        valid = True

                        for (dir, other_i, other_j) in directions_to_test:
                            other_dir = (dir + 2) % 4
                            other_tile = setup[other_i][other_j]
                            if not tile.match(dir, other_tile, other_dir):
                                valid = False
                                break

                        if valid:
                            setup[i][j] = tile
                            result = backtrack(new_remaining_tiles, setup)
                            if result is not None:
                                return result
                            
                            setup[i][j] = None
                
                tile.reset()

            return None
    return None



@profile
def part_one(entry: List[str]) -> int:
    tiles = []
    curr = 0
    for i in range(len(entry)):
        if len(entry[i]) == 0:
            tiles.append(Tile(entry[curr:i]))
            curr = i + 1
    
    grid_size = int(math.sqrt(len(tiles)))
    setup = [[None for _ in range(grid_size)] for __ in range(grid_size)]

    right_setup = backtrack(tiles, setup)
    assert(right_setup is not None)
    return right_setup[0][0].id * right_setup[0][-1].id * right_setup[-1][0]*id * right_setup[-1][-1].id

@profile
def part_two(entry: List[str]) -> int:
    return 0


if __name__ == "__main__":
    print("Part 1 example:", part_one(example_entries))
    print("Part 1 entry:", part_one(entries))

    print("Part 2 example:", part_two(example_entries))
    print("Part 2 entry:", part_two(entries))
