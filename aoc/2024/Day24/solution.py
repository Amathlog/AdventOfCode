import copy
from typing import List, Tuple, Dict, Optional, Set
from aoc.common.parse_entry import parse_all
from aoc.common.utils import profile
import re

entries, example_entries = parse_all(__file__, "entry.txt", "example.txt")

ops = {
    "AND": lambda x, y: x & y,
    "OR" : lambda x, y: x | y,
    "XOR": lambda x, y: x ^ y
}

class Operation:
    def __init__(self, wire1, op, wire2, wire3):
        self.wire1 = wire1
        self.wire2 = wire2
        self.wire3 = wire3
        self.op_name = op
        self.op = ops[op]

    def __call__(self, values: Dict[str, bool]):
        values[self.wire3] = self.op(values[self.wire1], values[self.wire2])

class Program:
    def __init__(self):
        self.operations: List[Operation] = []
        self.z_gates: List[str] = []
        self.outputs: Dict[str, Operation] = {}
        self.inputs : Dict[str, List[Operation]] = {}

    def cache_operations(self, existing_values: List[str], all_ops: List[str]):
        regex = re.compile("(\w+) (AND|OR|XOR) (\w+) \-\> (\w+)")
        retry = range(len(all_ops))
        seen_results = set(existing_values)
        self.outputs = {k: None for k in seen_results}

        while len(retry) > 0:
            new_retry = []
            for j in retry:
                wire1, op, wire2, wire3 = regex.findall(all_ops[j])[0]
                if wire1 not in seen_results or wire2 not in seen_results:
                    new_retry.append(j)
                else:
                    self.operations.append(Operation(wire1, op, wire2, wire3))
                    self.outputs[wire3] = self.operations[-1]
                    if wire1 not in self.inputs:
                        self.inputs[wire1] = []
                    if wire2 not in self.inputs:
                        self.inputs[wire2] = []
                    self.inputs[wire1].append(self.operations[-1])
                    self.inputs[wire2].append(self.operations[-1])
                    seen_results.add(wire3)
            retry = new_retry

        self.z_gates = sorted([g for g in seen_results if g[0] == "z"], key=lambda x: int(x[1:]), reverse=True)

    def swap(self, out1: str, out2: str):
        self.outputs[out1].wire3 = out2
        self.outputs[out2].wire3 = out1

    def unswap(self, out1: str, out2: str):
        self.outputs[out1].wire3 = out1
        self.outputs[out2].wire3 = out2

    def run_with_swap(self, x: int, y: int, out1: str, out2: str) -> int:
        self.swap(out1, out2)
         
        result = self.run_from_int(x, y, True)

        self.unswap(out1, out2)

        return result
        
    # Verified: 
    # * no z_gate depends on another z_gate
    # * no z bit depends on a higher bit from x and y (like z02 would depend on x03 for example)
    # * It seems like each input x and y for a given bit have 2 ops, one AND and one XOR
    def get_dependency_chain(self) -> Dict[str, Set[str]]:
        res = {}
        for z_gate in self.z_gates:
            dependencies = set()
            stack = [z_gate]
            while len(stack) > 0:
                curr = stack.pop()
                if curr in dependencies:
                    continue
                dependencies.add(curr)
                op = self.outputs[curr]
                if op is not None:
                    stack.extend([op.wire1, op.wire2])

            dependencies.remove(z_gate)
            res[z_gate] = dependencies

        return res

    def run_from_int(self, x: int, y: int, with_retry: bool = False) -> int:
        nb_bits = len(self.z_gates) - 1
        values = {}
        for i in range(nb_bits):
            values[f"x{i:02d}"] = bool(x & 1)
            x >>= 1
            values[f"y{i:02d}"] = bool(y & 1)
            y >>= 1

        if with_retry:
            return self.run_with_retry(values)
        else:
            return self.run(values)

    def run(self, init_values: Dict[str, bool]) -> int:
        values = {k: v for k, v in init_values.items()}
        for op in self.operations:
            op(values)

        result = 0
        for z_gate in self.z_gates:
            result <<= 1
            if values[z_gate]:
                result += 1
        
        return result
    
    def run_with_retry(self, init_values: Dict[str, bool]) -> int:
        retry = range(len(self.operations))
        values = {k: v for k, v in init_values.items()}
        while len(retry) > 0:
            new_retry = []
            for i in retry:
                op = self.operations[i]
                if op.wire1 not in values or op.wire2 not in values:
                    new_retry.append(i)
                else:
                    op(values)
            retry = new_retry

        result = 0
        for z_gate in self.z_gates:
            result <<= 1
            if values[z_gate]:
                result += 1
        
        return result

@profile
def part_one(entry: List[str]) -> int:
    i = 0
    values = {}
    for i in range(len(entry)):
        e = entry[i]
        if len(e) == 0:
            break

        wire, v = e.split(": ")
        values[wire] = bool(int(v))

    program = Program()
    program.cache_operations(values.keys(), entry[i+1:])
    return program.run(values)

@profile
def part_two(entry: List[str]) -> int:
    i = 0
    values = {}
    for i in range(len(entry)):
        e = entry[i]
        if len(e) == 0:
            break

        wire, v = e.split(": ")
        values[wire] = bool(int(v))

    program = Program()
    program.cache_operations(values.keys(), entry[i+1:])
    dependency_chain = program.get_dependency_chain()
    swaps = set()

    def verification(nb_bits: int, op1: str, op2: str):
        for i in range(-1, nb_bits):
            x = 1 << i if i >= 0 else 0
            for j in range(-1, nb_bits):
                y = 1 << j if j >= 0 else 0

                result = program.run_with_swap(x, y, op1.wire3, op2.wire3)
                if result != x+y:
                    return False
        return True

    for i in range(-1, len(program.z_gates) - 1):
        x = 1 << i if i >= 0 else 0
        for j in range(-1, len(program.z_gates) - 1):
            y = 1 << j if j >= 0 else 0

            result = program.run_from_int(x,y, True)
            if result != x+y:
                max_bit = max(i, j)
                z_gate = f"z{max_bit:02d}"

                all_ops = [gate for gate in dependency_chain[z_gate] if len(program.inputs[gate]) == 2]
                all_pairs = set()
                for op in all_ops:
                    pair = tuple(sorted([program.inputs[op][0].wire1, program.inputs[op][0].wire2]))
                    all_pairs.add(pair)

                for pair in all_pairs:
                    input1, input2 = pair
                    op1, op2 = program.inputs[input1]
                    if op1.wire3 in swaps or op2.wire3 in swaps:
                        continue

                    test = program.run_with_swap(x, y, op1.wire3, op2.wire3)
                    if test == x + y and verification(max_bit, op1, op2):
                        swaps.add(op1.wire3)
                        swaps.add(op2.wire3)
                        program.swap(op1.wire3, op2.wire3)
                        break

                if len(swaps) == 8:
                    break
        if len(swaps) == 8:
            break

    return ",".join(sorted(list(swaps)))

@profile
def part_two_bis(entry: List[str]):
    i = 0
    values = {}
    for i in range(len(entry)):
        e = entry[i]
        if len(e) == 0:
            break

        wire, v = e.split(": ")
        values[wire] = bool(int(v))

    program = Program()
    program.cache_operations(values.keys(), entry[i+1:])
    dependency_chain = program.get_dependency_chain()

    invalid_results = []
    nb_bits = len(program.z_gates) - 1
    for i in range(-1, nb_bits):
        x = 1 << i if i >= 0 else 0
        for j in range(-1, nb_bits):
            y = 1 << j if j >= 0 else 0

            result = program.run_from_int(x, y, True)
            if result != x+y:
                invalid_results.append((x, y))

    for x, y in invalid_results:
        nb_bits = max(len(bin(x)), len(bin(y))) - 2
        

    def shallow_verification():
        for x, y in invalid_results:
            result = program.run_from_int(x, y, True)
            if result != x+y:
                return False
        print("True")
        return True

    def verification():
        nb_bits = len(program.z_gates) - 1
        for i in range(-1, nb_bits):
            x = 1 << i if i >= 0 else 0
            for j in range(-1, nb_bits):
                y = 1 << j if j >= 0 else 0

                result = program.run_from_int(x, y, True)
                if result != x+y:
                    return False
        return True
    
    all_pairs = set()
    for gate in program.inputs.keys():
        if len(program.inputs[gate]) == 1:
            continue

        pair = tuple(sorted([program.inputs[gate][0].wire1, program.inputs[gate][0].wire2]))
        all_pairs.add(pair)

    all_pairs = list(all_pairs)
    length = len(all_pairs)
    for i in range(length):
        print(i)
        op1, op2 = program.inputs[all_pairs[i][0]]
        program.swap(op1.wire3, op2.wire3)
        for j in range(i+1, length):
            op3, op4 = program.inputs[all_pairs[j][0]]
            program.swap(op3.wire3, op4.wire3)
            for k in range(j+1, length):
                op5, op6 = program.inputs[all_pairs[k][0]]
                program.swap(op5.wire3, op6.wire3)
                for l in range(k+1, length):
                    op7, op8 = program.inputs[all_pairs[l][0]]
                    program.swap(op7.wire3, op8.wire3)
                    if shallow_verification() and verification():
                        return ",".join(sorted([op1.wire3, op2.wire3, op3.wire3, op4.wire3, op5.wire3, op6.wire3, op7.wire3, op8.wire3]))
                    program.unswap(op7.wire3, op8.wire3)
                program.unswap(op5.wire3, op6.wire3)
            program.unswap(op3.wire3, op4.wire3)
        program.unswap(op1.wire3, op2.wire3)

    return None


if __name__ == "__main__":
    print("Part 1 example:", part_one(example_entries))
    print("Part 1 entry:", part_one(entries))

    #print("Part 2 example:", part_two(example_entries))
    print("Part 2 entry:", part_two_bis(entries))
