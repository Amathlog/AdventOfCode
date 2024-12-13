import copy
from typing import List, Tuple, Dict, Optional, Set
from aoc.common.parse_entry import parse_all
from aoc.common.utils import profile
from aoc.common.point import Point
import re

entries, example_entries = parse_all(__file__, "entry.txt", "example.txt")

def is_int(v: float) -> Tuple[bool, int]:
    tolerance = 1e-3
    round_v = round(v)
    return round_v - tolerance <= v <= round_v + tolerance, round_v

def get_alpha_beta(button_a: Point, button_b: Point, prize: Point) -> Tuple[bool, int, int]:
    beta = (prize.y - (prize.x*button_a.y/button_a.x)) / (button_b.y - (button_b.x*button_a.y/button_a.x))
    alpha = (prize.x - beta * button_b.x) / button_a.x

    beta_int, beta = is_int(beta)
    alpha_int, alpha = is_int(alpha)

    return alpha_int and beta_int, alpha, beta

@profile
def solve(entry: List[str]) -> int:
    button_regex = re.compile("Button [AB]\: X\+(\d+), Y\+(\d+)")
    prize_regex = re.compile("Prize\: X\=(\d+), Y\=(\d+)")
    nb_tokens_part_1 = 0
    nb_tokens_part_2 = 0
    for i in range(len(entry) // 4 + 1):
        button_a = Point(*map(int, button_regex.findall(entry[4 * i])[0]))
        button_b = Point(*map(int, button_regex.findall(entry[4 * i + 1])[0]))
        prize = Point(*map(int, prize_regex.findall(entry[4 * i + 2])[0]))
        prize_part_B = prize + Point(10000000000000, 10000000000000)

        valid, alpha, beta = get_alpha_beta(button_a, button_b, prize)
        valid2, alpha2, beta2 = get_alpha_beta(button_a, button_b, prize_part_B)

        if valid:
            nb_tokens_part_1 += 3 * alpha + beta
        if valid2:
            nb_tokens_part_2 += 3 * alpha2 + beta2

    return nb_tokens_part_1, nb_tokens_part_2


if __name__ == "__main__":
    print("Part 1 and 2 example:", solve(example_entries))
    print("Part 1 and 2 entry:", solve(entries))
