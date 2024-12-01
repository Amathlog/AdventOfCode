import copy
from typing import List, Tuple, Dict, Optional, Set
from aoc.common.parse_entry import parse_all_multiple_parts, default_separator
from aoc.common.utils import profile
from aoc.common.point import Point
from aoc.common.grid import Grid

entries, example_entries = parse_all_multiple_parts(__file__, default_separator, 3, "entry.txt", "example.txt")

def extract_data(entry: List[str], should_split: bool):
    runic_words = entry[0].split(":")[1].split(",")
    sentences = []
    for e in entry[2:]:
        sentences.append(e.replace(",", ""))
        if (should_split):
            sentences[-1] = sentences[-1].split()

    return runic_words, sentences

def rolling(word: str, runic_word: str, previous_mask: list[int]) -> list[int]:
    mask = previous_mask
    for word_idx in range(len(word) - len(runic_word) + 1):
        i = 0
        while i < len(runic_word):
            if word[word_idx + i] != runic_word[i]:
                break
            i += 1
        
        if i == len(runic_word):
            for j in range(len(runic_word)):
                mask[word_idx + j] = 1

    return mask

def rolling_2D(word_matrix: Grid, runic_word: str, mask: Grid):
    up = Point(-1, 0)
    down = Point(1, 0)
    left = Point(0, -1)
    right = Point(0, 1)

    def step(p: Point, dir: Point):
        p += dir
        if not word_matrix.is_valid(p):
            p.y = (p.y + word_matrix.max_y) % word_matrix.max_y
        return p

    for i in range(word_matrix.max_x):
        for j in range(word_matrix.max_y):
            curr_pos = Point(i, j)
            if word_matrix[curr_pos] != runic_word[0]:
                continue

            curr_index = 1
            for dir in [up, down, left, right]:
                while curr_index < len(runic_word):
                    curr_pos = step(curr_pos, dir)

                    if not word_matrix.is_valid(curr_pos) or word_matrix[curr_pos] != runic_word[curr_index]:
                        break
                    curr_index += 1

                if curr_index == len(runic_word):
                    while curr_pos != Point(i, j):
                        mask[curr_pos] = 1
                        curr_pos = step(curr_pos, dir * -1)
                    mask[curr_pos] = 1

                curr_index = 1
                curr_pos = Point(i, j)

    return mask

@profile
def part_one(entry: List[str]) -> int:
    count = 0
    runic_words, sentences = extract_data(entry, True)
    for word in sentences[0]:
        for runic_word in runic_words:
            if runic_word in word:
                count += 1
    
    return count

@profile
def part_two(entry: List[str]) -> int:
    count = 0
    runic_words, sentences = extract_data(entry, True)
    for sentence in sentences:
        for word in sentence:
            mask = [0] * len(word)
            for runic_word in runic_words:
                mask = rolling(word, runic_word, mask)
                mask = rolling(word[::-1], runic_word, mask[::-1])[::-1]
            count += sum(mask)
    return count

@profile
def part_three(entry: List[str]) -> int:
    runic_words, word_matrix = extract_data(entry, False)
    word_matrix = Grid(word_matrix)
    mask = Grid([[0] * word_matrix.max_y for _ in range(word_matrix.max_x)])

    for runic_word in runic_words:
        mask = rolling_2D(word_matrix, runic_word, mask)

    return sum([sum(i) for i in mask.grid])


if __name__ == "__main__":
    print("Part 1 example:", part_one(example_entries[0]))
    print("Part 1 entry:", part_one(entries[0]))

    print("Part 2 example:", part_two(example_entries[1]))
    print("Part 2 entry:", part_two(entries[1]))

    print("Part 3 example:", part_three(example_entries[2]))
    print("Part 3 entry:", part_three(entries[2]))