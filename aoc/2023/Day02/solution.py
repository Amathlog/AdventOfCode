from __future__ import annotations
from pathlib import Path
import os
from typing import List
from aoc.common.parse_entry import parse_all

entries, example_entries = parse_all(__file__, "entry.txt", "example.txt")


class Draw:
    def __init__(self, red: int = 0, green: int = 0, blue: int = 0):
        self.red = red
        self.green = green
        self.blue = blue

    def update_max(self, other: Draw) -> Draw:
        if (other.red > self.red):
            self.red = other.red
        if (other.green > self.green):
            self.green = other.green
        if (other.blue > self.blue):
            self.blue = other.blue

    def __repr__(self) -> str:
        return f"{self.red} red, {self.green} green, {self.blue} blue"
    
    def __gt__(self, other: Draw) -> bool:
        return self.red > other.red or self.green > other.green or self.blue > other.blue


class Game:
    def __init__(self, entry: str):
        game, rest = entry.split(": ")
        self.game_id = int(game[5:])

        self.draws: List[Draw] = []
        for draw in rest.split("; "):
            final_draw = Draw()
            for color_n in draw.split(", "):
                n, color = color_n.split(" ")
                setattr(final_draw, color, int(n))
            self.draws.append(final_draw)

    def __repr__(self) -> str:
        return f"Game {self.game_id}: " + "; ".join([str(draw) for draw in self.draws])


def part_one(entries: List[str], draw_limit: Draw):
    games = [Game(entry) for entry in entries]
    res = 0
    for game in games:
        game_valid = True
        for draw in game.draws:
            if draw > draw_limit:
                game_valid = False
                break
        if game_valid:
            res += game.game_id

    return res


def part_two(entries: List[str]):
    games = [Game(entry) for entry in entries]
    res = 0
    for game in games:
        max_draw = Draw()
        for draw in game.draws:
            max_draw.update_max(draw)
        res += (max_draw.red * max_draw.green * max_draw.blue)

    return res

 
if __name__ == "__main__":
    draw_limit = Draw(12, 13, 14)
    print("Part 1 example:", part_one(example_entries, draw_limit))
    print("Part 1 entry:", part_one(entries, draw_limit))

    print("Part 2 example:", part_two(example_entries))
    print("Part 2 entry:", part_two(entries))
