from pathlib import Path
import os
from typing import List

entry_file = Path(os.path.abspath(__file__)).parent / "entry.txt"

with entry_file.open("r") as f:
    entries = f.readlines()

for i in range(len(entries)):
    if entries[i][-1] == '\n':
        entries[i] = entries[i][:-1]

class Board:
    def __init__(self, data: List[str]):
        self.data = [[int(x) for x in s.split(' ') if len(x) > 0] for s in data]

    def mark(self, number):
        found = False
        for i in range(len(self.data)):
            for j in range(len(self.data[i])):
                if self.data[i][j] == number:
                    found = True
                    self.data[i][j] = 0
                    break
            if found:
                break

        if found:
            return self.check_win(i, j)

        return False

    def check_win(self, i: int, j: int):
        # Check column
        won = True
        for i_ in range(len(self.data)):
            if self.data[i_][j] != 0:
                won = False
                break
        
        if won:
            return True

        won = True
        for j_ in range(len(self.data[i])):
            if self.data[i][j_] != 0:
                won = False
                break
        
        return won


numbers = [int(x) for x in entries[0].split(",")]
boards = []
i = 2
while i < len(entries):
    boards.append((len(boards), Board(entries[i:i+5])))
    i += 6

import copy

done = False
remaining_boards = []

import numpy as np

first_board = None
last_board = None

for n in numbers:
    for i, b in boards:
        if b.mark(n):
            unmarked = np.sum(b.data)
            res = unmarked * n
            if first_board is None:
                first_board = (i, res)
            if len(boards) == 1:
                last_board = (i, res)
        else:
            remaining_boards.append((i, b))
    
    boards = remaining_boards
    if len(boards) == 0:
        break
    remaining_boards = []

print("First answer: Board {}, score = {}".format(*first_board))
print("Second answer: Board {}, score = {}".format(*last_board))