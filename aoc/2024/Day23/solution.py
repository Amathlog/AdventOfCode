import copy
from typing import List, Tuple, Dict, Optional, Set
from aoc.common.parse_entry import parse_all
from aoc.common.utils import profile

entries, example_entries = parse_all(__file__, "entry.txt", "example.txt")

class Computer:
    def __init__(self, name: str):
        self.name = name
        self.connections: Set["Computer"] = set()

    def add_connection(self, other: "Computer"):
        self.connections.add(other)
        other.connections.add(self)

    def __hash__(self):
        return hash(self.name)
    
    def __eq__(self, value):
        return self.name == value.name
    
    def __lt__(self, other):
        return self.name < other.name
    
    def __repr__(self):
        return self.name
    
    def is_t(self):
        return self.name[0] == "t"

@profile
def part_one(entry: List[str]) -> int:
    all_computers: Dict[str, Computer] = {}
    for e in entry:
        cpu1, cpu2 = e.split("-")
        if cpu1 not in all_computers:
            all_computers[cpu1] = Computer(cpu1)
        if cpu2 not in all_computers:
            all_computers[cpu2] = Computer(cpu2)
        all_computers[cpu1].add_connection(all_computers[cpu2])

    interconnected = set()
    nb_t_s = 0
    max_seq = None

    for c in all_computers.values():
        for other in c.connections:
            for other2 in other.connections:
                if c in other2.connections:
                    seq = tuple(sorted([c, other, other2]))
                    if seq not in interconnected:
                        interconnected.add(seq)
                        if any((seq[0].is_t(), seq[1].is_t(), seq[2].is_t())):
                            nb_t_s += 1
            
            temp = c.connections.intersection(other.connections)
            if len(temp) > 0:
                if max_seq is not None and len(max_seq) >= (len(temp) + 2):
                    continue
            
                potential_seq = tuple(sorted([c, other] + list(temp)))
                valid = True
                while len(temp) > 0:
                    cpu1 = temp.pop()
                    if temp.intersection(cpu1.connections) != temp:
                        valid = False
                        break

                if valid:
                    max_seq = potential_seq    

    return nb_t_s, ",".join([c.name for c in max_seq])

@profile
def part_two(entry: List[str]) -> int:
    return 0


if __name__ == "__main__":
    print("Part 1 example:", part_one(example_entries))
    print("Part 1 entry:", part_one(entries))

    print("Part 2 example:", part_two(example_entries))
    print("Part 2 entry:", part_two(entries))
