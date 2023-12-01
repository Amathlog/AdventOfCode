from pathlib import Path
import os
import copy
from typing import List, Tuple, Dict
from aoc.common.parse_entry import parse_entry

entry_file = Path(os.path.abspath(__file__)).parent / "entry.txt"
example_file = Path(os.path.abspath(__file__)).parent / "example.txt"
example_file2 = Path(os.path.abspath(__file__)).parent / "example2.txt"

entries = parse_entry(entry_file)
example_entries = parse_entry(example_file)
example_entries2 = parse_entry(example_file2)

dictionary = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9
}

reverse_dictionary = {k[::-1]: v for k,v in dictionary.items()}

def is_digit(c) -> bool:
    return ord('0') <= ord(c) <= ord('9')


def find_first_digit(s: str, reverse: bool) -> Tuple[int, int]:
    string_to_check = s[::-1] if reverse else s
    for i, c in enumerate(string_to_check):
        if is_digit(c):
            return i, int(c)
    return None, None


def find_first_word_digit(s: str, reverse: bool) -> Tuple[int, int]:
    string_to_check = s[::-1] if reverse else s

    current_index = None
    current_value = None

    for word, value in (reverse_dictionary if reverse else dictionary).items():
        index = string_to_check.find(word)
        if index != -1 and (current_index is None or index < current_index):
            current_index = index
            current_value = value

        # If it is the first item of the string, we can't find a better prospect, so stop there.
        if index == 0:
            break

    return current_index, current_value


def find_first_word_or_digit(s: str, reverse: bool) -> int:
    first_word = find_first_word_digit(s, reverse)
    first_digit = find_first_digit(s, reverse)

    if first_word[0] is None or (first_digit[0] is not None and first_word[0] > first_digit[0]):
        return first_digit[1]
    else:
        return first_word[1]


def part_one(all_entries: List[str]):
    res = 0
    for entry in all_entries:
        first_value = find_first_digit(entry, False)[1]
        second_value = find_first_digit(entry, True)[1]
        
        assert first_value is not None and second_value is not None
        res += first_value * 10 + second_value
    return res
        

def part_two(all_entries: List[str]):
    res = 0
    for entry in all_entries:
        first_value = find_first_word_or_digit(entry, False)
        second_value = find_first_word_or_digit(entry, True)
        
        assert first_value is not None and second_value is not None
        res += first_value * 10 + second_value
    return res


if __name__ == "__main__":
    print("Part 1 example:", part_one(example_entries))
    print("Part 1 entry:", part_one(entries))

    print("Part 2 example:", part_two(example_entries2))
    print("Part 2 entry:", part_two(entries))
