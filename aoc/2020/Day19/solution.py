import copy
from typing import List, Tuple, Dict, Optional, Set
from aoc.common.parse_entry import parse_all
from aoc.common.utils import profile
import re
import abc

entries, example_entries = parse_all(__file__, "entry.txt", "example.txt")

class BaseRule(abc.ABC):
    def __init__(self, id: int):
        self.id = id

    @abc.abstractmethod
    def max_size(self) -> int:
        return 0

    @abc.abstractmethod
    def min_size(self) -> int:
        return 0

    @abc.abstractmethod
    def satisfy(self, input: str) -> int:
        return 0


class Axiom(BaseRule):
    def __init__(self, id: int, char: str):
        super().__init__(id)
        self.char = char

    def satisfy(self, input: str) -> int:
        if len(input) > 0 and self.char == input[0]:
            return 1
        else:
            return -1
    
    def max_size(self):
        return 1
    
    def min_size(self):
        return 1
    
    def __repr__(self):
        return f"{self.id}: \"{self.char}\""


class Rule(BaseRule):
    def __init__(self, id: int, rules: Tuple[BaseRule]):
        super().__init__(id)
        self.rules = rules
        self.cached_max_size = None
        self.cached_min_size = None

    def satisfy(self, input: str):
        if len(input) < self.min_size():
            return -1
        
        i = 0
        for rule in self.rules:
            offset = rule.satisfy(input[i:])
            if offset == -1:
                return -1
            i += offset
        
        return i
    
    def max_size(self):
        if self.cached_max_size is None:
            self.cached_max_size = self.max_size_internal()
        
        return self.cached_max_size
    
    def min_size(self):
        if self.cached_min_size is None:
            self.cached_min_size = self.min_size_internal()
        
        return self.cached_min_size
    
    def max_size_internal(self):
        return sum((r.max_size() for r in self.rules))
    
    def min_size_internal(self):
        return sum((r.min_size() for r in self.rules))
    
    def __repr__(self):
        rules_str = [str(r.id) for r in self.rules]
        return f"{self.id}: {' '.join(rules_str)}"


class Conjunction(BaseRule):
    def __init__(self, id: int, left_rule: BaseRule, right_rule: BaseRule):
        super().__init__(id)
        self.left_rule = left_rule
        self.right_rule = right_rule

        self.cached_max_size = None
        self.cached_min_size = None

    def satisfy(self, input):
        if len(input) < self.min_size():
            return -1
        
        left_offset = self.left_rule.satisfy(input)
        if left_offset == -1:
            return self.right_rule.satisfy(input)
        else:
            return left_offset
        
    def max_size(self):
        if self.cached_max_size is None:
            self.cached_max_size = self.max_size_internal()
        
        return self.cached_max_size
    
    def min_size(self):
        if self.cached_min_size is None:
            self.cached_min_size = self.min_size_internal()
        
        return self.cached_min_size
        
    def max_size_internal(self):
        return max(self.left_rule.max_size(), self.right_rule.max_size())
    
    def min_size_internal(self):
        return min(self.left_rule.min_size(), self.right_rule.min_size())
    
    def __repr__(self):
        return f"{self.id}: {' '.join([str(r.id) for r in self.left_rule.rules])} | {' '.join([str(r.id) for r in self.right_rule.rules])}"


def make_grammar(input: List[str]) -> Dict[int, BaseRule]:
    grammar: Dict[int, BaseRule] = {}

    grammar_str: Dict[int, str] = {}
    for line in input:
        rule_id, syntax = line.split(": ")
        grammar_str[int(rule_id)] = syntax

    stack = [0]
    while len(stack) > 0:
        rule_id = stack.pop()
        rule_id = int(rule_id)

        if rule_id in grammar:
            continue

        syntax = grammar_str[rule_id]

        def gather_rule_ids(syntax: str) -> Tuple[bool, Tuple[int]]:
            subrule_ids = tuple(map(int, syntax.split()))
            all_rules_computed = True
            for subrule_id in subrule_ids:
                if subrule_id not in grammar:
                    if all_rules_computed:
                        all_rules_computed = False
                        stack.append(rule_id)
                    stack.append(subrule_id)
            
            return all_rules_computed, subrule_ids

        if syntax[0] == "\"":
            grammar[rule_id] = Axiom(rule_id, syntax[1])
        elif "|" in syntax:
            left_syntax, right_syntax = syntax.split(" | ")

            left_ok, left_ids = gather_rule_ids(left_syntax)
            right_ok, right_ids = gather_rule_ids(right_syntax)

            if left_ok and right_ok:
                left_rule = Rule(-1, tuple((grammar[i] for i in left_ids)))
                right_rule = Rule(-1, tuple((grammar[i] for i in right_ids)))
                grammar[rule_id] = Conjunction(rule_id, left_rule, right_rule)
        else:
            ok, ids = gather_rule_ids(syntax)
            if ok:
                grammar[rule_id] = Rule(rule_id, tuple((grammar[i] for i in ids)))

    return grammar

@profile
def part_one(entry: List[str]) -> int:
    i = 0
    while len(entry[i]) > 0:
        i += 1

    grammar = make_grammar(entry[:i])
    rule_zero = grammar[0]
    rule_zero_min = rule_zero.min_size()
    rule_zero_max = rule_zero.max_size()

    i += 1
    count = 0
    for line in entry[i:]:
        if len(line) < rule_zero_min or len(line) > rule_zero_max:
            continue
        offset = rule_zero.satisfy(line)
        if offset != -1:
            count += 1
    return count

@profile
def part_two(entry: List[str]) -> int:
    return 0


if __name__ == "__main__":
    print("Part 1 example:", part_one(example_entries))
    print("Part 1 entry:", part_one(entries))

    print("Part 2 example:", part_two(example_entries))
    print("Part 2 entry:", part_two(entries))
