import copy
from typing import List, Tuple, Dict, Optional, Set
from aoc.common.parse_entry import parse_all
from aoc.common.utils import profile
from multiprocessing import Process, Value, Event
import time
from ctypes import c_size_t

entries, example_entries = parse_all(__file__, "entry.txt", "example.txt")

class Interpreter:
    def __init__(self, reg_a: int, reg_b: int, reg_c: int, program: List[int]):
        self.reg_a = reg_a
        self.reg_b = reg_b
        self.reg_c = reg_c
        self.sp = 0
        self.program = program
        self.output = []

    def fetch(self) -> Tuple[int, int]:
        opcode = self.program[self.sp]
        operand = self.program[self.sp+1]
        self.sp += 2

        # Combo
        if opcode in [0, 2, 5, 6, 7]:
            if operand == 4:
                operand = self.reg_a
            elif operand == 5:
                operand = self.reg_b
            elif operand == 6:
                operand = self.reg_c
            elif operand == 7:
                assert(False)

        return opcode, operand

    def exec(self, break_on_mismatch: bool =False) -> bool:       
        while self.sp < len(self.program) - 1:
            opcode, operand = self.fetch()
            if opcode == 0:
                self.adv(operand)
            elif opcode == 1:
                self.bxl(operand)
            elif opcode == 2:
                self.bst(operand)
            elif opcode == 3:
                self.jnz(operand)
            elif opcode == 4:
                self.bxc(operand)
            elif opcode == 5:
                self.out(operand)
                if break_on_mismatch:
                    if len(self.output) > len(self.program):
                        return False
                    for i in range(len(self.output)):
                        if self.output[i] != self.program[i]:
                            return False
            elif opcode == 6:
                self.bdv(operand)
            elif opcode == 7:
                self.cdv(operand)
            else:
                assert(False)

        return True
        

    def adv(self, operand: int):
        self.reg_a //= (2**operand)

    def bxl(self, operand: int):
        self.reg_b ^= operand
    
    def bst(self, operand: int):
        self.reg_b = operand % 8
    
    def jnz(self, operand: int):
        if self.reg_a != 0:
            self.sp = operand

    def bxc(self, operand: int):
        self.reg_b ^= self.reg_c

    def out(self, operand: int):
        self.output.append(operand % 8)

    def bdv(self, operand: int):
        self.reg_b = self.reg_a // (2**operand)

    def cdv(self, operand: int):
        self.reg_c = self.reg_a // (2**operand)


@profile
def part_one(entry: List[str]) -> int:
    reg_a = int(entry[0].split(": ")[1])
    reg_b = int(entry[1].split(": ")[1])
    reg_c = int(entry[2].split(": ")[1])
    p = entry[4].split(": ")[1]
    program = [int(c) for c in p.split(",")]

    interpreter = Interpreter(reg_a, reg_b, reg_c, program)
    interpreter.exec()
    return ",".join([str(i) for i in interpreter.output])

def process(nb_threads: int, index: int, reg_b: int, reg_c: int, program: List[int], stop: Event, result, track):
    reg_a = index
    while True:
        interpreter = Interpreter(reg_a, reg_b, reg_c, program)
        if interpreter.exec(True) and interpreter.output == program:
            with result.get_lock():
                if result.value == 0 or reg_a < result.value:
                    result.value = reg_a
            stop.set()
            break
        
        reg_a += nb_threads

        if reg_a % 1000000 == 0:
            if stop.is_set():
                break
            if track is not None:
                track.value = reg_a

@profile
def part_two(entry: List[str]) -> int:
    last_not_working = 245706000000

    track = Value(c_size_t, 0)
    result = Value(c_size_t, 0)
    stop = Event()
    reg_b = int(entry[1].split(": ")[1])
    reg_c = int(entry[2].split(": ")[1])
    p = entry[4].split(": ")[1]
    program = [int(c) for c in p.split(",")]

    nb_threads = 31
    processes = [Process(target=process, args=(nb_threads, last_not_working, reg_b, reg_c, program, stop, result, track if i == 0 else None)) for i in range(nb_threads)]
    for p in processes:
        p.start()

    while not stop.is_set():
        time.sleep(5)
        print(track.value)

    for p in processes:
        p.join()

    return result.value


if __name__ == "__main__":
    print("Part 1 example:", part_one(example_entries))
    print("Part 1 entry:", part_one(entries))

    print("Part 2 example:", part_two(example_entries))
    print("Part 2 entry:", part_two(entries))
