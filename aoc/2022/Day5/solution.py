from pathlib import Path
import os
import copy
from typing import Optional

class Instruction:
    def __init__(self, n: int, c_from: int, c_to: int):
        self.n = n
        self.c_from = c_from
        self.c_to = c_to

    @staticmethod
    def from_input(input: str) -> "Instruction":
        _, n, __, c_from, ___, c_to = input.split(" ")
        return Instruction(int(n), int(c_from), int(c_to))

    def __repr__(self) -> str:
        return f"move {self.n} from {self.c_from} to {self.c_to}"

class Stack:
    def __init__(self, id: int):
        self.id = id
        self.stack = []

    def insert(self, crate: str):
        self.stack.append(crate)

    def __len__(self) -> int:
        return len(self.stack)

    def move(self, n: int, other: "Stack", keep_order: bool):
        assert len(self) >= n

        if keep_order:
            other.stack.extend(self.stack[-n:])
        else:
            other.stack.extend(self.stack[-1:-n-1:-1])

        self.stack = self.stack[:-n]

    def top(self) -> Optional[str]:
        return None if len(self.stack) == 0 else self.stack[-1]

class Cargo:
    def __init__(self, n_stacks: int):
        # Stack id starts at 1
        self.stacks = [Stack(i + 1) for i in range(n_stacks)]

    def execute(self, inst: Instruction, keep_order: bool):
        self.stacks[inst.c_from - 1].move(inst.n, self.stacks[inst.c_to - 1], keep_order)

    def __repr__(self) -> str:
        res = ""
        max_size = max([len(s) for s in self.stacks])

        for i in reversed(range(max_size)):
            for stack in self.stacks:
                if len(stack) <= i:
                    res += "    "
                else:
                    res += f"[{stack.stack[i]}] "
            res += "\n"
        
        return res

    @staticmethod
    def construct(input: list[str]) -> "Cargo":
        nb_stacks = (len(input[0]) + 1) // 4
        cargo = Cargo(nb_stacks)

        for e in input[::-1]:
            i = 1
            for stack in cargo.stacks:
                if (e[i] != " "):
                    stack.insert(e[i])
                i += 4

        return cargo

    def top(self) -> str:
        return "".join([s.top() for s in self.stacks])

entry_file = Path(os.path.abspath(__file__)).parent / "entry.txt"
example_file = Path(os.path.abspath(__file__)).parent / "example.txt"

with entry_file.open("r") as f:
    entries = f.readlines()

for i in range(len(entries)):
    if entries[i][-1] == '\n':
        entries[i] = entries[i][:-1]

# First cut the input in 2, one with the crates, one with the instructions
crates = []
instructions = []

for i, e in enumerate(entries):
    if (len(e) < 2 or e[1] == '1'):
        continue

    # m for move
    if (e[0] == "m"):
        instructions = [Instruction.from_input(e_) for e_ in entries[i:]]
        break

    crates.append(e)

cargo = Cargo.construct(crates)
cargo2 = copy.deepcopy(cargo)

for inst in instructions:
    cargo.execute(inst, keep_order=False)
    cargo2.execute(inst, keep_order=True)

print(f"Part 1: Top for stacks = {cargo.top()}")
print(f"Part 2: Top for stacks = {cargo2.top()}")
