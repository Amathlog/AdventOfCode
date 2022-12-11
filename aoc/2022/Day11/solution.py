from pathlib import Path
import os
import copy
from typing import List, Callable

entry_file = Path(os.path.abspath(__file__)).parent / "entry.txt"
example_file = Path(os.path.abspath(__file__)).parent / "example.txt"

with entry_file.open("r") as f:
    entries = f.readlines()

for i in range(len(entries)):
    if entries[i][-1] == '\n':
        entries[i] = entries[i][:-1]

class Item:
    def __init__(self, level: int):
        self.level = level

    def update_before_throw(self):
        self.level //= 3

    def __repr__(self) -> str:
        return str(self.level)


class Monkey:
    def __init__(self, id: int, init_items: List[Item], update_rule: Callable[[int], int], throw_rule: Callable[[Item, List["Monkey"], bool], None]):
        self.items = init_items
        self.update_rule = update_rule
        self.throw_rule = throw_rule
        self.id = id
        self.nb_inspected_items = 0

    def take_turn(self, monkeys: List["Monkey"], relief: bool = True):
        for item in self.items:
            item.level = self.update_rule(item.level)
            self.throw_rule(item, monkeys, relief)

        self.nb_inspected_items += len(self.items)
        self.items.clear()
        
    def receive(self, item: Item):
        self.items.append(item)

    def __repr__(self) -> str:
        return f"Monkey {self.id} holds {self.items} and has inspected {self.nb_inspected_items} items"

    @staticmethod
    def from_input(inputs: List[str]) -> "Monkey":
        _, id = inputs[0].split(" ")
        id = int(id[:-1])

        _, items = inputs[1].split(":")
        items = [Item(int(item)) for item in items.split(",")]

        _, ops = inputs[2].split(" = ")
        _, op, other = ops.split(" ")
        update_rule = UpdateRule(op, other)

        _, divide = inputs[3].split(" by ")
        divide = int(divide)

        _, true_monkey = inputs[4].split(" monkey ")
        true_monkey = int(true_monkey)

        _, false_monkey = inputs[5].split(" monkey ")
        false_monkey = int(false_monkey)

        throw_rule = ThrowRule(divide, true_monkey, false_monkey)
        
        return Monkey(id, items, update_rule, throw_rule)


class ThrowRule:
    mul_divide = 1
    def __init__(self, divide: int, true_monkey: int, false_monkey: int):
        self.divide = divide
        self.true_monkey = true_monkey
        self.false_monkey = false_monkey
        ThrowRule.mul_divide *= self.divide

    def __call__(self, item: Item, monkeys: List[Monkey], relief: bool):
        if relief:
            item.update_before_throw()
        else:
            item.level %= ThrowRule.mul_divide

        if item.level % self.divide == 0:
            monkeys[self.true_monkey].receive(item)
        else:
            monkeys[self.false_monkey].receive(item)


class UpdateRule:
    def __init__(self, op: str, other: str):
        self.op = op
        self.itself = other == "old"
        self.other_n = 0 if self.itself else int(other)

    def __call__(self, old: int):
        if self.itself:
            res = old * old
        else:
            if self.op == "+":
                res = old + self.other_n
            else:
                res = old * self.other_n

        return res

def print_monkeys(monkeys: List[Monkey]):
    for monkey in monkeys:
        print(monkey)
    print("-----")

if __name__ == "__main__":
    monkeys1: List[Monkey] = []

    for i in range(len(entries) // 7 + 1):
        monkeys1.append(Monkey.from_input(entries[7 * i: 7 * (i + 1)]))

    monkeys2 = copy.deepcopy(monkeys1)

    monkeys = [monkeys1, monkeys2]

    all_rounds = [20, 10000]

    # print("At start:")
    # print_monkeys(monkeys)

    for j, nb_rounds in enumerate(all_rounds):
        verbose = j == 0
        relief = j == 0

        for i in range(nb_rounds):
            for monkey in monkeys[j]:
                monkey.take_turn(monkeys[j], relief)
        
            if verbose or (i == 0 or i == 19 or i % 500 == 499):
                #print(f"After round {i+1}:")
                #print_monkeys(monkeys[j])
                pass

        sorted_monkeys = sorted(monkeys[j], key=lambda x: x.nb_inspected_items, reverse=True)
        monkey_business = sorted_monkeys[0].nb_inspected_items * sorted_monkeys[1].nb_inspected_items
        print(f"Part {j + 1}: Monkey business after {nb_rounds} = {monkey_business}")

