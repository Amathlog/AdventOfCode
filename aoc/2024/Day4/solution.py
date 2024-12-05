import copy
from typing import List, Tuple, Dict, Optional, Set
from aoc.common.parse_entry import parse_all
from aoc.common.utils import profile
from aoc.common.grid import Grid, Point

entries, example_entries = parse_all(__file__, "entry.txt", "example.txt")

up = Point(-1, 0)
down = Point(1, 0)
left = Point(0, -1)
right = Point(0, 1)

def rolling(word_matrix: Grid, pos: Point, dir: Point, word_to_find: str):
    curr_index = 1
    curr_pos = pos
    while curr_index < len(word_to_find):
        curr_pos += dir

        if not word_matrix.is_valid(curr_pos) or word_matrix[curr_pos] != word_to_find[curr_index]:
            break
        curr_index += 1

    return curr_index == len(word_to_find)

@profile
def part_one(entry: List[str]) -> int:
    dirs = [up, down, left, right, up + left, up + right, down + left, down + right]
    word_matrix = Grid(entry)

    word_to_find = "XMAS"
    count = 0

    for i in range(word_matrix.max_x):
        for j in range(word_matrix.max_y):
            pos = Point(i, j)
            if word_matrix[pos] != word_to_find[0]:
                continue

            for dir in dirs:
                pos = Point(i, j)
                if rolling(word_matrix, pos, dir, word_to_find):
                    count += 1

    return count

@profile
def part_two(entry: List[str]) -> int:
    word_matrix = Grid(entry)

    words_to_find = ["MAS", "SAM"]
    count = 0
    diag_left = down + left
    diag_right = down + right

    def get_word_to_find(pos: Point) -> str:
        if not word_matrix.is_valid(pos):
            return ""
        if word_matrix[pos] == words_to_find[0][0]:
            return words_to_find[0]
        elif word_matrix[pos] == words_to_find[1][0]:
            return words_to_find[1]
        else:
            return ""

    for i in range(word_matrix.max_x):
        for j in range(word_matrix.max_y):
            curr_pos = Point(i, j)
            word_to_find = get_word_to_find(curr_pos)
            if word_to_find == "":
                continue

            if rolling(word_matrix, curr_pos, diag_right, word_to_find):
                new_pos = Point(i, j+2)
                word_to_find = get_word_to_find(new_pos)
                if word_to_find == "":
                    continue

                if rolling(word_matrix, new_pos, diag_left, word_to_find):
                    count += 1

    return count


if __name__ == "__main__":
    print("Part 1 example:", part_one(example_entries))
    print("Part 1 entry:", part_one(entries))

    print("Part 2 example:", part_two(example_entries))
    print("Part 2 entry:", part_two(entries))
