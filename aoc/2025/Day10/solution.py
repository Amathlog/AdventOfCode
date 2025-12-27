import copy
from typing import List, Tuple, Dict, Optional, Set, Any
from aoc.common.parse_entry import parse_all
from aoc.common.utils import profile
import re
from aoc.common.astar import AStar_Solver
import math

entries, example_entries = parse_all(__file__, "entry.txt", "example.txt")

target_regex = re.compile(r"\[([\.#]+)\]")
buttons_regex = re.compile(r"\(((?:\d,?)*)\)")
joltage_regex = re.compile(r"\{((?:\d,?)*)\}")

class Machine():
    def __init__(self, target: int, buttons: List[Tuple[int, ...]], joltage: Tuple[int, ...]):
        self.target = target
        self.buttons = buttons
        self.joltage = joltage

    @staticmethod
    def construct(entry: str) -> "Machine":
        target = sum([(1 if c == "#" else 0) << i for i,c in enumerate(target_regex.findall(entry)[0])])
        buttons = [tuple(map(int, b.split(","))) for b in buttons_regex.findall(entry)]
        joltage = tuple(map(int, joltage_regex.findall(entry)[0].split(",")))

        nb_bits_joltage = sum((0 if j == 0 else math.ceil(math.log2(j)) for j in joltage))
        print(nb_bits_joltage)

        return Machine(target, buttons, joltage)
    
class MachineOnline(AStar_Solver):
    def __init__(self, machine):
        super().__init__()
        self.machine = machine

    def get_neighbors(self, state: int) -> List[int]:
        states = set()
        for button in self.machine.buttons:
            curr = state
            for i in button:
                curr = curr ^ (1 << i)
            
            states.add(curr)

        return list(states)

    def get_cost(self, state: int) -> int:
        return 1

    def is_start(self, state: int) -> bool:
        return state == 0
    
    def is_end(self, state: int) -> bool:
        return state == self.machine.target
    
    def get_start_states(self) -> List[int]:
        return [0]
    
class MachineJoltage(AStar_Solver):
    def __init__(self, machine: Machine):
        super().__init__()
        self.machine = machine
        self.start = (0,) * len(machine.joltage)

    def get_neighbors(self, state: Tuple[int]) -> List[Tuple[int]]:
        states = []
        for button in self.machine.buttons:
            curr = list(state)
            valid = True
            for i in button:
                curr[i] += 1
                if curr[i] > self.machine.joltage[i]:
                    valid = False
                    break
            if valid:
                states.append(tuple(curr))

        return states

    def get_cost(self, state: Tuple[int]) -> int:
        return 1
    
    def heuristic(self, state: Tuple[int]):
        temp = 0
        for i in range(len(state)):
            temp += (self.machine.joltage[i] - state[i])
        
        return temp / len(state)

    def is_start(self, state: Tuple[int]) -> bool:
        return state == self.start
    
    def is_end(self, state: Tuple[int]) -> bool:
        return state == self.machine.joltage
    
    def get_start_states(self) -> List[Tuple[int]]:
        return [self.start]


@profile
def solve(entry: List[str]) -> int:
    machines = [Machine.construct(e) for e in entry]
    result_1 = 0
    result_2 = 0
    for machine in machines:
        path_1 = MachineOnline(machine).solve()
        result_1 += len(path_1) - 1

        path_2 = MachineJoltage(machine).solve()
        result_2 += len(path_2) - 1

        print("Done")

    return result_1, result_2

@profile
def part_two(entry: List[str]) -> int:
    return 0


if __name__ == "__main__":
    print("Part 1 and 2 example:", solve(example_entries))
    print("Part 1 and 2 entry:", solve(entries))
