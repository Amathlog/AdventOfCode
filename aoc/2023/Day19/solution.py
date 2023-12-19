import copy
from typing import List, Tuple, Dict, Optional, Set
from aoc.common.parse_entry import parse_all
from aoc.common.utils import profile

entries, example_entries = parse_all(__file__, "entry.txt", "example.txt")

class Part:
    def __init__(self, x: int, m: int, a: int, s: int) -> None:
        self.x = x
        self.m = m
        self.a = a
        self.s = s
    
    def sum(self) -> int:
        return self.x + self.m + self.a + self.s
    
    def __eq__(self, other: "Part") -> bool:
        return self.x == other.x and self.m == other.m and self.a == other.a and self.s == other.s
    
    def __hash__(self) -> int:
        return hash((self.x, self.m, self.a, self.s))
    
    @staticmethod
    def construct(e: str) -> "Part":
        x, m, a, s = e[1:-1].split(",")
        return Part(int(x[2:]), int(m[2:]), int(a[2:]), int(s[2:]))
    
class Range:
    def __init__(self, x, m, s, a) -> None:
        self.x = x
        self.m = m
        self.a = a
        self.s = s

    def num_combinaisons(self) -> int:
        x_diff = self.x[1] - self.x[0] + 1
        m_diff = self.m[1] - self.m[0] + 1
        a_diff = self.a[1] - self.a[0] + 1
        s_diff = self.s[1] - self.s[0] + 1

        assert(x_diff > 0 and m_diff > 0 and a_diff > 0 and s_diff > 0)

        return x_diff * m_diff * a_diff * s_diff

    @staticmethod
    def initial_range() -> "Range":
        return Range([1, 4000], [1, 4000], [1, 4000], [1, 4000])
    
class Condition:
    def __init__(self, attr: str, less: bool, num: int) -> None:
        assert(attr in ["x", "m", "a", "s"])
        self.attr = attr
        self.less = less
        self.num = num

    def satisfy(self, part: Part) -> bool:
        value = getattr(part, self.attr) 
        if self.less:
            return value < self.num
        else:
            return value > self.num
    
    # First range satisfy condition, second doesn't
    def split(self, _range: Range) -> Tuple[Optional[Range], Optional[Range]]:
        value = getattr(_range, self.attr)
        if self.less:
            if value[0] >= self.num or value[1] < self.num:
                return None, _range
            else:
                first_range = copy.deepcopy(_range)
                second_range = copy.deepcopy(_range)
                setattr(first_range, self.attr, [value[0], self.num - 1])
                setattr(second_range, self.attr, [self.num, value[1]])

                return first_range, second_range
        else:
            if value[0] > self.num or value[1] <= self.num:
                return None, _range
            else:
                first_range = copy.deepcopy(_range)
                second_range = copy.deepcopy(_range)
                setattr(first_range, self.attr, [value[0], self.num])
                setattr(second_range, self.attr, [self.num + 1, value[1]])

                return second_range, first_range

        
    @staticmethod
    def construct(e: str) -> Optional["Condition"]:
        less_split = e.split("<")
        if len(less_split) == 2:
            num, _ = less_split[1].split(":")
            return Condition(less_split[0], True, int(num))
        
        greater_split = e.split(">")
        if len(greater_split) == 2:
            num, _ = greater_split[1].split(":")
            return Condition(greater_split[0], False, int(num))
        
        return None
        
class Workflow:
    def __init__(self, name: str, conditions_workflow: List[Tuple[Optional[Condition], str]]):
        self.conditions_workflow = conditions_workflow
        self.name = name

    def next_workflow(self, part: Part) -> str:
        for condition, workflow in self.conditions_workflow:
            if condition is None or condition.satisfy(part):
                return workflow
            
        assert(False)

    def split(self, _range: Range) -> List[Tuple[str, Range]]:
        res = []
        curr = _range
        for condition, workflow in self.conditions_workflow:
            if condition is None:
                res.append((workflow, curr))
            else:
                satisfy_range, curr = condition.split(curr)
                if satisfy_range is not None:
                    res.append((workflow, satisfy_range))
                if curr is None:
                    break
        
        return res

    @staticmethod
    def construct(e: str) -> "Workflow":
        name, rest = e.split("{")
        conditions_workflow = []
        for c in rest[:-1].split(","):
            condition = Condition.construct(c)
            if condition is None:
                conditions_workflow.append((None, c))
            else:
                conditions_workflow.append((condition, c.split(":")[-1]))
        return Workflow(name, conditions_workflow)

@profile
def part_one(entry: List[str]) -> int:
    # Workflows
    workflows: dict[str, Workflow] = {}
    i = 0
    while len(entry[i]) > 0:
        workflow = Workflow.construct(entry[i])
        workflows[workflow.name] = workflow
        i += 1

    # Parts
    parts = list(map(Part.construct, entry[i+1:]))

    res = 0
    for p in parts:
        curr_workflow = "in"
        while curr_workflow not in ["A", "R"]:
            curr_workflow = workflows[curr_workflow].next_workflow(p)

        if curr_workflow == "A":
            res += p.sum()

    return res
        

@profile
def part_two(entry: List[str]) -> int:
    # Workflows
    workflows: dict[str, Workflow] = {}
    i = 0
    while len(entry[i]) > 0:
        workflow = Workflow.construct(entry[i])
        workflows[workflow.name] = workflow
        i += 1

    ranges = [("in", Range.initial_range())]
    valid_ranges = []
    while len(ranges) > 0:
        workflow, _range = ranges.pop()
        if workflow == "A":
            valid_ranges.append(_range)
            continue
        elif workflow == "R":
            continue

        ranges.extend(workflows[workflow].split(_range))

    return sum(map(Range.num_combinaisons, valid_ranges))


if __name__ == "__main__":
    print("Part 1 example:", part_one(example_entries))
    print("Part 1 entry:", part_one(entries))

    print("Part 2 example:", part_two(example_entries))
    print("Part 2 entry:", part_two(entries))
