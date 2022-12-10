from pathlib import Path
import os
import copy
from enum import Enum
import math
from typing import List
from reprint import output
import time

entry_file = Path(os.path.abspath(__file__)).parent / "entry.txt"
example_file = Path(os.path.abspath(__file__)).parent / "example.txt"

with entry_file.open("r") as f:
    entries = f.readlines() 

for i in range(len(entries)):
    if entries[i][-1] == '\n':
        entries[i] = entries[i][:-1]


class Direction(Enum):
    Right = (1, 0)
    Left = (-1, 0)
    Up = (0, 1)
    Down = (0, -1)


class Position:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def is_touching(self, other: "Position"):
        return abs(self.x - other.x) <= 1 and abs(self.y - other.y) <= 1

    def move_towards(self, other: "Position"):
        if self.is_touching(other):
            return

        dir_x = other.x - self.x
        dir_y = other.y - self.y

        if (dir_x != 0):
            self.x += 1 if dir_x > 0 else -1
        if (dir_y != 0):
            self.y += 1 if dir_y > 0 else -1

    def move(self, dir: Direction, n: int = 1):
        self.x += n * dir.value[0]
        self.y += n * dir.value[1]

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    def __eq__(self, other: "Position"):
        return self.x == other.x and self.y == other.y

    def __repr__(self) -> str:
        return str((self.x, self.y))


class Status:
    def __init__(self, nb_knots: int = 2):
        assert nb_knots >= 2 and nb_knots <= 10
        self.knots_pos = [Position(0, 0) for _ in range(nb_knots)]
        self.tail_visited = set([copy.deepcopy(self.knots_pos[-1])])
        self.step_count = 0

    def print_progress(self):
        print(f"Step {self.step_count}: Head = {self.knots_pos[0]} ; Tail = {self.knots_pos[-1]}")

    def step(self, dir: Direction, verbose: bool = False):
        self.knots_pos[0].move(dir)
        for i in range(1, len(self.knots_pos)):
            self.knots_pos[i].move_towards(self.knots_pos[i - 1])
        self.step_count += 1
        if self.knots_pos[-1] not in self.tail_visited:
            self.tail_visited.add(copy.deepcopy(self.knots_pos[-1]))

        if verbose:
            self.print_progress()

    def to_grid_string(self, min_pos: Position, max_pos: Position) -> List[List[str]]:
        max_height = 35
        max_width = 150
        height = max_pos.y - min_pos.y + 1
        width = max_pos.x - min_pos.x + 1

        # If it is too big, center the grid around 0,0 and move it so everything is visible
        if height > max_height:
            height = max_height
            min_pos.y = -max_height // 2
            max_pos.y = max_height // 2

            min_y = min([p.y for p in self.knots_pos])
            max_y = max([p.y for p in self.knots_pos])

            if max_y > max_pos.y:
                max_pos.y = max_y
                min_pos.y = max_pos.y - max_height
            elif min_y < min_pos.y:
                min_pos.y = min_y
                max_pos.y = min_pos.y + max_height

        if width > max_width:
            width = max_width
            min_pos.x = -max_width // 2
            max_pos.x = max_width // 2

            min_x = min([p.x for p in self.knots_pos])
            max_x = max([p.x for p in self.knots_pos])

            if max_x > max_pos.x:
                max_pos.x = max_x
                min_pos.x = max_pos.x - max_width
            elif min_x < min_pos.x:
                min_pos.x = min_x
                max_pos.x = min_pos.x + max_width

        if height < 0 or width < 0:
            return ""

        res = [["."] * width for _ in range(height)]

        def set_char(pos: Position, char: str):
            trans = Position(pos.x - min_pos.x, max_pos.y - pos.y)
            if trans.x < 0 or trans.y < 0 or trans.x >= width or trans.y >= height:
                return
            res[trans.y][trans.x] = char

        for tail in self.tail_visited:
            set_char(tail, "#")

        set_char(Position(0, 0), "s")
        for i in reversed(range(len(self.knots_pos))):
            if i == len(self.knots_pos) - 1:
                char = "T"
            elif i == 0:
                char = "H"
            else:
                char = str(i)

            set_char(self.knots_pos[i], char)

        return res

    @property
    def head_pos(self) -> Position:
        return self.knots_pos[0]

    @property
    def tail_pos(self) -> Position:
        return self.knots_pos[-1]

            
class Recorder:
    def __init__(self, initial_status: Status):
        self.status = copy.deepcopy(initial_status)
        self.directions: List[Direction] = []
        self.min_pos = Position(0, 0)
        self.max_pos = Position(0, 0)

    def update(self, status: Status, dir: Direction):
        self.directions.append(dir)
        self.min_pos.x = min(self.min_pos.x, status.head_pos.x)
        self.min_pos.y = min(self.min_pos.y, status.head_pos.y)
        self.max_pos.x = max(self.max_pos.x, status.head_pos.x)
        self.max_pos.y = max(self.max_pos.y, status.head_pos.y)

    def replay(self, nb_steps: int = 1, step_time: float = 0.2):
        temp = self.status.to_grid_string(self.min_pos, self.max_pos)
        height, width = len(temp), len(temp[0])
        i = 0
        with output(initial_len=height+1, interval=0) as output_lines:
            while i < len(self.directions):
                for _ in range(nb_steps):
                    self.status.step(self.directions[i])
                    i += 1
                grid = self.status.to_grid_string(self.min_pos, self.max_pos)
                for j in range(len(grid)):
                    output_lines[j+1] = "".join(grid[j])
                time.sleep(step_time)


status = Status(2)
status2 = Status(10)
recorder = Recorder(status)
recorder2 = Recorder(status2)

for e in entries:
    dir, count = e.split(" ")
    if dir == 'L':
        dir = Direction.Left
    elif dir == 'U':
        dir = Direction.Up
    elif dir == 'D':
        dir = Direction.Down
    else:
        dir = Direction.Right

    for i in range(int(count)):
        status.step(dir)
        status2.step(dir)
        recorder.update(status, dir)
        recorder2.update(status2, dir)

# recorder2.replay(nb_steps=5, step_time=0.001)

print(f"Part 1: Number of tiles visited by tail {len(status.tail_visited)}")
print(f"Part 2: Number of tiles visited by tail {len(status2.tail_visited)}")

    