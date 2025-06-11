import copy
from typing import List, Tuple, Dict, Optional, Set
from aoc.common.parse_entry import parse_all
from aoc.common.utils import profile

entries, example_entries = parse_all(__file__, "entry.txt", "example.txt")

numbers = [str(i) for i in range(10)]

def parse_operand(input: str):
    count = 0
    i = 0
    for i, c in enumerate(input):
        if c == '(':
            count += 1
        if c == ')':
            count -= 1

        if count == 0:
            break

    if i != 0:
        return (True, i)
    else:
        while i < len(input) and input[i] in numbers:
            i += 1
        return (False, i)

class Num(int):
    def evaluate(self) -> int:
        return self
    
    def evaluate_prio(self) -> int:
        return self

class Op:
    def __init__(self, entry: str):
        self.operands = []
        self.ops = []

        # Parse the right first
        left_prio, left_limit = parse_operand(entry)

        if left_prio:
            self.operands.append(Op(entry[1:left_limit]))
            left_limit += 1
        else:
            self.operands.append(Num(int(entry[0:left_limit])))

        if left_limit < len(entry):
            self.ops.append(entry[left_limit])

            # Create a new op and append it
            temp_op = Op(entry[left_limit+1:])

            self.operands.extend(temp_op.operands)
            self.ops.extend(temp_op.ops)

    def evaluate(self) -> int:
        curr = self.operands[0].evaluate()       
        for i in range(len(self.ops)):
            next = self.operands[i+1].evaluate()
            if self.ops[i] == "+":
                curr += next
            else:
                curr *= next

        return curr

    def evaluate_prio(self) -> int:
        # First evaluate all adds
        temp_results = []
        i = 0
        while i < len(self.ops):
            curr = self.operands[i].evaluate_prio()
            while i < len(self.ops) and self.ops[i] == "+":
                i += 1
                curr += self.operands[i].evaluate_prio()
            temp_results.append(curr)
            i += 1
        if i == len(self.ops):
            temp_results.append(self.operands[-1].evaluate_prio())

        # Then evaluate all the mult
        curr = temp_results[0]
        for i in range(1, len(temp_results)):
            curr *= temp_results[i]
        
        return curr
        
    def __repr__(self):
        res = "("
        for i in range(len(self.ops)):
            res += str(self.operands[i]) + self.ops[i]
        
        return res + str(self.operands[-1]) + ")"

@profile
def part(entry: List[str]) -> int:
    res1 = []
    res2 = []
    for line in entry:
        line = line.replace(' ', '')
        op = Op(line)
        #print(f"Entry: {line} ; op: {str(op)}")
        res1.append(op.evaluate())
        res2.append(op.evaluate_prio())
    return sum(res1), sum(res2)

@profile
def part_two(entry: List[str]) -> int:
    return 0


if __name__ == "__main__":
    print("Part 1 and 2 example:", part(example_entries))
    print("Part 1 and 2 entry:", part(entries))
