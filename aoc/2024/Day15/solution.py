import copy
from typing import List, Tuple, Dict, Optional, Set
from aoc.common.parse_entry import parse_all
from aoc.common.utils import profile
from aoc.common.grid import Grid
from aoc.common.point import Point, up, down, left, right
from enum import Enum, auto

entries, example_entries = parse_all(__file__, "entry.txt", "example.txt")

dir_map = {'^': up, '>': right, '<': left, 'v': down}

class Cell(Enum):
    Wall = "#"
    Empty = "."
    Box = "O"
    BoxLeft = "["
    BoxRight = "]"

cell_map = {'#': Cell.Wall, '.': Cell.Empty, 'O': Cell.Box}

def extract_data(entry: List[str], big_cells: bool = False) -> Tuple[Grid, Point, List[Point]]:
    grid = []
    move_sequence = []
    start_pos = None
    i = 0
    while len(entry[i]) != 0:
        grid.append([])
        for j, c in enumerate(entry[i]):
            if c == "@":
                y = 2 * j if big_cells else j
                start_pos = Point(i,2*j)
                c = "."

            if c == "O" and big_cells:
                grid[-1].append(Cell.BoxLeft)
                grid[-1].append(Cell.BoxRight)
            else:
                grid[-1].append(cell_map[c])
                if big_cells:
                    grid[-1].append(cell_map[c])

        i += 1

    assert(start_pos is not None)
    for line in entry[i+1:]:
        for c in line:
            move_sequence.append(dir_map[c])
    
    return Grid(grid), start_pos, move_sequence

def print_grid(grid: Grid, robot_pos: Point):
    res = ""
    for i in range(grid.max_x):
        for j in range(grid.max_y):
            if robot_pos.x == i and robot_pos.y == j:
                res += "@"
            else:
                res += grid.get(i,j).value
        res += "\n"
    print(res)

def step(grid: Grid, robot_pos: Point, dir: Point) -> Point:
    temp = robot_pos + dir
    if not grid.is_valid(temp) or grid[temp] == Cell.Wall:
        return robot_pos
    elif grid[temp] == Cell.Empty:
        return temp
    
    assert(grid[temp] == Cell.Box)
    
    curr = temp
    while grid[curr] == Cell.Box:
        curr = curr + dir

    if grid[curr] == Cell.Wall:
        return robot_pos
    
    assert(grid[curr] == Cell.Empty)
    grid[temp] = Cell.Empty
    grid[curr] = Cell.Box
    return temp

def step_bigcells(grid: Grid, robot_pos: Point, dir: Point) -> Point:
    temp = robot_pos + dir
    if not grid.is_valid(temp) or grid[temp] == Cell.Wall:
        return robot_pos
    elif grid[temp] == Cell.Empty:
        return temp
    
    assert(grid[temp] in [Cell.BoxLeft, Cell.BoxRight])
    
    boxes = []
    if dir in [left, right]:
        curr = temp
        while grid[curr] in [Cell.BoxLeft, Cell.BoxRight]:
            boxes.append(curr)
            curr = curr + dir

        if grid[curr] == Cell.Wall:
            return robot_pos
        
        assert(grid[curr] == Cell.Empty)
        for b in boxes[::-1]:
            assert(grid[b+dir] != Cell.Wall)
            grid[b + dir] = grid[b]
        grid[temp] = Cell.Empty

        return temp
    
    stack = [temp]
    boxes = {}
    while len(stack) > 0:
        curr = stack.pop()
        if grid[curr] == Cell.Wall:
            return robot_pos
        elif grid[curr] == Cell.Empty:
            continue

        if curr in boxes:
            continue

        assert(grid[temp] in [Cell.BoxLeft, Cell.BoxRight])
        other = (curr + left) if grid[curr] == Cell.BoxRight else (curr + right)

        boxes[curr] = grid[curr]
        boxes[other] = grid[other]
        temp_1 = curr + dir
        temp_2 = other + dir
        stack.extend((temp_1, temp_2))
    
    assert(len(boxes) % 2 == 0)
    seen_positions = set(boxes.keys())
    for b_pos, b_type in boxes.items():
        new_pos = b_pos+dir
        assert(grid[new_pos] != Cell.Wall)
        grid[new_pos] = b_type
        if new_pos in seen_positions:
            seen_positions.remove(new_pos)

    for b in seen_positions:
        grid[b] = Cell.Empty
    
    return temp

def verify_grid(grid) -> bool:
    for i in range(grid.max_x):
        for j in range(grid.max_y):
            if grid.get(i, j) == Cell.BoxLeft and grid.get(i,j+1) != Cell.BoxRight:
                return False
            if grid.get(i, j) == Cell.BoxRight and grid.get(i, j-1) != Cell.BoxLeft:
                return False
    return True

@profile
def part_one(entry: List[str]) -> int:
    grid, pos, move_sequence = extract_data(entry)
    for move in move_sequence:
        pos = step(grid, pos, move)

    result = 0
    for i in range(grid.max_x):
        for j in range(grid.max_y):
            if grid.get(i, j) == Cell.Box:
                result += 100 * i + j
    
    return result

@profile
def part_two(entry: List[str]) -> int:
    grid, pos, move_sequence = extract_data(entry, True)

    for i, move in enumerate(move_sequence):
        pos = step_bigcells(grid, pos, move)

    result = 0
    for i in range(grid.max_x):
        for j in range(grid.max_y):
            if grid.get(i, j) == Cell.BoxLeft:
                result += 100 * i + j

    return result

if __name__ == "__main__":
    print("Part 1 example:", part_one(example_entries))
    print("Part 1 entry:", part_one(entries))

    print("Part 2 example:", part_two(example_entries))
    print("Part 2 entry:", part_two(entries))
