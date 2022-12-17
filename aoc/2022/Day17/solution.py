from pathlib import Path
import os
import copy
from typing import List, Tuple, Dict
import enum
from collections import namedtuple

Position = namedtuple("Position", ["x", "y"])

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

class Type(enum.Enum):
    Air = "."
    Rock = "#"


class Grid:
    def __init__(self, width: int):
        self.width = width
        self.height = 0
        self.grid: List[List[Type]] = []
        self.current_max_height = 0
        self.grid_offset = 0

        self.extend_grid(1)

    def extend_grid(self, new_height: int):
        if self.height >= new_height:
            return

        self.grid.extend([[Type.Air for _ in range(self.width)] for __ in range(new_height - self.height)])
        assert len(self.grid) == (new_height - self.grid_offset)
        self.height = new_height

    def __getitem__(self, position: Position):
        return self.grid[position.y][position.x]

    def __setitem__(self, position: Position, new_type: Type):
        self.grid[position.y][position.x] = new_type

    def fix_block(self, block: "Block"):
        all_y = set()
        for pos in block.all_tiles_positions_gen():
            assert self[pos] == Type.Air
            self[pos] = Type.Rock
            all_y.add(pos.y)
        
        tentative_max_height = self.grid_offset + block.position.y + block.top_most_offset + 1
        if tentative_max_height > self.current_max_height:
            self.current_max_height = tentative_max_height

        self.offset_grid(all_y)

    def offset_grid(self, all_lines: set[int]):
        all_lines = sorted(list(all_lines), reverse=True)
        for y in all_lines:
            full_blocked = True
            blocked = True
            for x in range(self.width):
                if self[Position(x, y)] != Type.Rock:
                    full_blocked = False
                    if y == 0 or self[Position(x, y - 1)] != Type.Rock:
                        blocked = False
                        break
                
            if blocked:
                # Can cut 1 line higher if the line if full blocked.
                if full_blocked:
                    y += 1
                #print(self)
                #print("===== CUT =====")
                offset = y
                assert offset > 0
                self.grid = self.grid[offset:]
                self.grid_offset += y
                #print(self)
                break

    def to_string(self, temporary_block: "Block") -> str:
        temp_pos = set((temporary_block.all_tiles_positions_gen())) if temporary_block is not None else set()
        res = ""
        for j, line in enumerate(self.grid[::-1]):
            res += "|"
            for i, t in enumerate(line):
                pos = Position(i, self.height - self.grid_offset - j - 1)
                if pos in temp_pos:
                    res += "@"
                else:
                    res += t.value
            res += "|\n"
        res += "+" + "-" * self.width + "+\n"
        return res
            
    def __repr__(self) -> str:
        return self.to_string(None)


class Block:
    def __init__(self, all_tiles_offset: List[Position]):
        self.position: Position = None
        self.all_tiles_offset = all_tiles_offset

        self.left_most_offset = min((p.x for p in all_tiles_offset))
        self.right_most_offset = max((p.x for p in all_tiles_offset))
        self.top_most_offset = max((p.y for p in all_tiles_offset))
        self.bot_most_offset = min((p.y for p in all_tiles_offset))

        self.width = self.right_most_offset - self.left_most_offset + 1
        self.height = self.top_most_offset - self.bot_most_offset + 1

    def all_tiles_positions_gen(self, x_offset: int = 0, y_offset: int = 0):
        for tile in self.all_tiles_offset:
            yield Position(self.position.x + tile.x + x_offset, self.position.y + tile.y + y_offset)

    def will_collide(self, grid: Grid, x_offset: int, y_offset: int) -> bool:
        for pos in self.all_tiles_positions_gen(x_offset, y_offset):
            if pos.x < 0 or pos.x >= grid.width or pos.y < 0 or grid[pos] == Type.Rock:
                return True

        return False

    def go_down(self):
        self.position = Position(self.position.x, self.position.y - 1)

    def go_left(self):
        self.position = Position(self.position.x - 1, self.position.y)
    
    def go_right(self):
        self.position = Position(self.position.x + 1, self.position.y)

    def spawn_block(self, grid: Grid) -> "Block":
        res = copy.deepcopy(self)
        x_pos = 2 - self.left_most_offset
        y_pos = grid.current_max_height + 3 - self.bot_most_offset
        grid.extend_grid(y_pos + self.top_most_offset + 1)

        res.position = Position(x_pos, y_pos - grid.grid_offset)
        return res


def simulate(entry: str, max_count: int):
    all_blocks = [
        # @@@@
        Block([Position(-2, 0), Position(-1, 0), Position(0, 0), Position(1, 0)]),
        #  @ 
        # @@@
        #  @
        Block([Position(0, 1), Position(-1, 0), Position(0, 0), Position(1, 0), Position(0, -1)]),
        #   @
        #   @
        # @@@
        Block([Position(-2, 0), Position(-1, 0), Position(0, 0), Position(0, 1), Position(0, 2)]),
        # @
        # @
        # @
        # @
        Block([Position(0, 2), Position(0, 1), Position(0, 0), Position(0, -1)]),
        # @@
        # @@
        Block([Position(0, 1), Position(1, 1), Position(0, 0), Position(1, 0)])
    ]

    grid = Grid(7)
    current_block_index = 0
    current_entry_index = 0
    count = 0

    while count < max_count:
        current_block = all_blocks[current_block_index % len(all_blocks)].spawn_block(grid)
        #print(grid.to_string(current_block))

        while True:
            # first try to move it accroding to entry
            dir = entry[current_entry_index]
            if dir == "<" and not current_block.will_collide(grid, -1, 0):
                current_block.go_left()
            elif dir == ">" and not current_block.will_collide(grid, 1, 0):
                current_block.go_right()
            #print("Direction:", dir)
            current_entry_index += 1
            if current_entry_index >= len(entry):
                current_entry_index = 0

            if current_block.will_collide(grid, 0, -1):
                grid.fix_block(current_block)
                break
            current_block.go_down()
            #print(grid.to_string(current_block))
        
        current_block_index += 1
        if current_block_index >= len(all_blocks):
            current_block_index = 0
        count += 1

    print(f"Part 1: Size after {max_count} blocks = {grid.current_max_height}")


if __name__ == "__main__":
    import time
    e = entries
    x = simulate(e[0], 2022)
    start = time.perf_counter()
    x = simulate(e[0], 100000)
    print(f"Time taken = {time.perf_counter() - start} s")

    start = time.perf_counter()
    x = simulate(e[0], 5000)
    print(f"Time taken = {time.perf_counter() - start} s")