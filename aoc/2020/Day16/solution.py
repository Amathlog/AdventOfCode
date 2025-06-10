import copy
from typing import List, Tuple, Dict, Optional, Set
from aoc.common.parse_entry import parse_all
from aoc.common.utils import profile
import re

entries, example_entries, example2_entries = parse_all(__file__, "entry.txt", "example.txt", "example2.txt")

class Range:
    def __init__(self, min: str, max: str):
        self.min = int(min)
        self.max = int(max)

    def valid(self, value: int):
        return self.min <= value <= self.max
    
    def __repr__(self):
        return f"{self.min}-{self.max}"
    
    def __eq__(self, value):
        return self.min == value.min and self.max == value.max
    
    def __hash__(self):
        return hash((self.min, self.max))

class Rule:
    def __init__(self, s, min_1, max_1, min_2, max_2):
        self.name = s
        self.range_1 = Range(min_1, max_1)
        self.range_2 = Range(min_2, max_2)

    def valid(self, v: int):
        return self.range_1.valid(v) or self.range_2.valid(v)
    
    def __repr__(self):
        return f"{self.name}: {self.range_1} or {self.range_2}"
    
    def __eq__(self, value):
        return self.name == value.name and self.range_1 == value.range_1 and self.range_2 == value.range_2
    
    def __hash__(self):
        return hash((self.name, self.range_1, self.range_2))


rule_regex = re.compile("(.+): (\d+)\-(\d+) or (\d+)\-(\d+)")

def get_rules(input: List[str]):
    res = []
    for i in input:
        res.append(Rule(*rule_regex.findall(i)[0]))
    return res

def get_all(input: List[str]):
    i = 0
    while len(input[i]) != 0:
        i += 1

    rules = get_rules(input[:i])
    i += 2

    your_ticket = list(map(int, input[i].split(',')))
    i += 3
    nearby_tickets = []
    while i < len(input):
        nearby_tickets.append(list(map(int, input[i].split(','))))
        i += 1

    return rules, your_ticket, nearby_tickets


@profile
def part_one(entry: List[str]) -> int:
    rules, _, tickets = get_all(entry)
    res = 0
    for ticket in tickets:
        for v in ticket:
            valid = False
            for rule in rules:
                if rule.valid(v):
                    valid = True
                    break
            if not valid:
                res += v

    return res

@profile
def part_two(entry: List[str]) -> int:
    rules, my_ticket, nearby_tickets = get_all(entry)
    valid_tickets = []
    for ticket in nearby_tickets:
        ticket_is_valid = True
        for v in ticket:
            valid = False
            for rule in rules:
                if rule.valid(v):
                    valid = True
                    break
            if not valid:
                ticket_is_valid = False
                break
        if ticket_is_valid:
            valid_tickets.append(ticket)

    def validate(rule: Rule, i: int):
        for ticket in valid_tickets:
            if not rule.valid(ticket[i]):
                return False
        
        return True
    
    # For each number, find the valid assignments
    valid_assignments: List[List[Rule]] = []
    for i in range(len(rules)):
        valid_assignments.append([])
        for r in rules:
            if validate(r, i):
                valid_assignments[-1].append(r)

    len_valid_assignments = [len(v) for v in valid_assignments]
    indices = sorted(range(len(rules)), key= lambda i: len_valid_assignments[i])

    # Build the possible assignment with backtracking
    assignment = [0] * len(rules)
    i = 0
    while i < len(rules):
        idx_i = indices[i]
        valid = True
        for j in range(i):
            idx_j = indices[j]
            if valid_assignments[idx_j][assignment[j]] == valid_assignments[idx_i][assignment[i]]:
                valid = False
                break
        
        if not valid:
            while i >= 0:
                assignment[i] += 1
                if assignment[i] >= len(valid_assignments[indices[i]]):
                    assignment[i] = 0
                    i -= 1
                    continue
                break
        else:
            i += 1

    real_assignment = [None for _ in range(len(rules))]
    for i in range(len(rules)):
        real_assignment[indices[i]] = valid_assignments[indices[i]][assignment[i]]

    res = 1
    for i, a in enumerate(real_assignment):
        assert(a.valid(my_ticket[i]))
        if "departure" in a.name:
            res *= my_ticket[i]

    return res

if __name__ == "__main__":
    print("Part 1 example:", part_one(example_entries))
    print("Part 1 entry:", part_one(entries))

    #print("Part 2 example:", part_two(example2_entries))
    print("Part 2 entry:", part_two(entries))
