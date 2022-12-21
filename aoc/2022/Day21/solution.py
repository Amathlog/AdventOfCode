from pathlib import Path
import os
import copy
from typing import List, Tuple, Dict

entry_file = Path(os.path.abspath(__file__)).parent / "entry.txt"
example_file = Path(os.path.abspath(__file__)).parent / "example.txt"

def parse_entry(path: str) -> List[str]:
    with path.open("r") as f:
        entries = f.readlines()

    for i in range(len(entries)):
        if entries[i][-1] == '\n':
            entries[i] = entries[i][:-1]

    return entries

entries = parse_entry(entry_file)
example_entries = parse_entry(example_file)

class Unknown:
    def __init__(self):
        self.op_list = []

    def solve(self, other_value: int):
        curr = other_value
        while len(self.op_list) > 0:
            op, other, self_is_left = self.op_list.pop()
            if op == "-":
                curr = curr - other
            elif op == "//":
                curr = curr // other
            elif op == "+":
                if self_is_left:
                    curr = curr + other
                else:
                    curr = other - curr
            elif op == "*":
                if self_is_left:
                    curr = curr * other
                else:
                    curr = other // curr

        return curr

    def add(self, other, self_is_left: bool):
        self.op_list.append(("-", other, True))
        return self

    def sub(self, other, self_is_left: bool):
        self.op_list.append(("+", other, self_is_left))
        return self

    def mul(self, other, self_is_left: bool):
        self.op_list.append(("//", other, True))
        return self

    def div(self, other, self_is_left: bool):
        self.op_list.append(("*", other, self_is_left))
        return self


class Monkey:
    def __init__(self, input: str):
        self.name, other = input.split(":")
        other = other[1:]
        self.value = None
        try:
            self.value = int(other)
        except ValueError:
            self.name1, self.op, self.name2 = other.split(" ")
            if self.op == "/":
                self.op = "//"
    
    def get_value(self, monkeys: Dict[str, "Monkey"]) -> int:
        if self.value is None:
            value1 = monkeys[self.name1].get_value(monkeys)
            value2 = monkeys[self.name2].get_value(monkeys)
            self.value = eval(f"{value1}{self.op}{value2}")
        
        return self.value

    def get_value2(self, monkeys: Dict[str, "Monkey"]):
        if self.value is None:
            value1 = monkeys[self.name1].get_value2(monkeys)
            value2 = monkeys[self.name2].get_value2(monkeys)

            if self.name == "root":
                if type(value1) is Unknown:
                    return value1.solve(value2)
                else:
                    return value2.solve(value1)
            
            unknown = None
            if type(value1) is Unknown:
                assert type(value2) is not Unknown
                unknown = value1
                other = value2
                self_is_left = True
            elif type(value2) is Unknown:
                assert type(value1) is not Unknown
                unknown = value2
                other = value1
                self_is_left = False

            if unknown is not None:
                if self.op == "+":
                    unknown.add(other, self_is_left)
                elif self.op == "-":
                    unknown.sub(other, self_is_left)
                elif self.op == "*":
                    unknown.mul(other, self_is_left)
                elif self.op == "//":
                    unknown.div(other, self_is_left)
                else:
                    assert False

                self.value = unknown
            else:
                self.value = eval(f"{value1}{self.op}{value2}")

        return self.value


def solve(entries: List[str]):
    monkeys = {}
    for e in entries:
        monkey = Monkey(e)
        monkeys[monkey.name] = monkey

    print("Part 1: Root yells =", monkeys["root"].get_value(monkeys))

def solve2(entries: List[str]):
    monkeys = {}
    for e in entries:
        monkey = Monkey(e)
        monkeys[monkey.name] = monkey

    monkeys["humn"].value = Unknown()

    print("Part 1: Root yells =", monkeys["root"].get_value2(monkeys))

if __name__ == "__main__":
    print("Example:")
    solve(example_entries)
    solve2(example_entries)
    print("Entries:")
    solve(entries)
    solve2(entries)