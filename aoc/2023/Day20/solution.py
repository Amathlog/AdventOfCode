import copy
from typing import List, Tuple, Dict, Optional, Set
from aoc.common.parse_entry import parse_all
from aoc.common.utils import profile
import abc

entries, example_entries = parse_all(__file__, "entry.txt", "example.txt")

class Module(abc.ABC):
    def __init__(self, name: str, connections: List[str]) -> None:
        self.name = name
        self.connections = connections
        
    def update_input_connection(self, input_connection: str):
        pass

    # Return a list of (Origin, Destination, Pulse)
    def pulse(self, pulse_origin: str, input_pulse: bool) -> List[Tuple[str, str, bool]]:
        return [(self.name, c, input_pulse) for c in self.connections]
    
    @staticmethod
    def construct(module_name: str, connections: List[str]) -> "Module":
        assert(module_name != "")
        if module_name[0] == "%":
            return FilpFlop(module_name[1:], connections)
        elif module_name[0] == "&":
            return Conjunction(module_name[1:], connections)
        else:
            return Module(module_name, connections)
    
class FilpFlop(Module):
    def __init__(self, name: str, connections: List[str]) -> None:
        super().__init__(name, connections)
        self.state = False

    def pulse(self, pulse_origin: str, input_pulse: bool) -> List[Tuple[str, str, bool]]:
        if input_pulse:
            return []

        self.state = not self.state
        return [(self.name, c, self.state) for c in self.connections]
    
class Conjunction(Module):
    def __init__(self, name: str, connections: List[str]) -> None:
        super().__init__(name, connections)
        self.input_connections: List[str] = []
        self.memory: Dict[str, bool] = {}

    def update_input_connection(self, input_connection: str):
        if input_connection not in self.input_connections:
            self.input_connections.append(input_connection)
            self.memory[input_connection] = False

    def pulse(self, pulse_origin: str, input_pulse: bool) -> List[Tuple[str, str, bool]]:
        self.memory[pulse_origin] = input_pulse
        output_pulse = not all(self.memory.values())
        return [(self.name, c, output_pulse) for c in self.connections]
    
def print_pulse(transition: Tuple[str, str, bool]):
    print(f"{transition[0]} -{'high' if transition[2] else 'low'}-> {transition[1]}")

def construct_modules(entry: List[str]):
    modules: Dict[str, Module] = {"button": Module("button", ["broadcaster"])}
    for e in entry:
        module_name, connections = e.replace(" ", "").split("->")
        if module_name not in modules:
            new_module = Module.construct(module_name, connections.split(","))
            modules[new_module.name] = new_module

    for name, m in modules.items():
        for c in m.connections:
            if c not in modules:
                continue
            modules[c].update_input_connection(name)
    
    return modules

@profile
def part_one(entry: List[str], times: int) -> int:
    modules = construct_modules(entry)

    low_pulses = 0
    high_pulses = 0

    for _ in range(times):
        pulses = modules["button"].pulse("null", False)
        while len(pulses) > 0:
            origin, dest, pulse = pulses.pop(0)
            if pulse:
                high_pulses += 1
            else:
                low_pulses += 1
            
            #print_pulse((origin, dest, pulse))
            if dest not in modules:
                continue

            pulses.extend(modules[dest].pulse(origin, pulse))

    print(low_pulses, high_pulses)
    return low_pulses * high_pulses

@profile
def part_two(entry: List[str]) -> int:
    modules = construct_modules(entry)
    
    button_presses = 0
    done = False
    while not done:
        button_presses += 1
        pulses = modules["button"].pulse("null", False)
        while len(pulses) > 0:
            origin, dest, pulse = pulses.pop(0)

            if dest == "rx" and not pulse:
                done = True
                break
            
            #print_pulse((origin, dest, pulse))
            if dest not in modules:
                continue

            pulses.extend(modules[dest].pulse(origin, pulse))

    return button_presses


if __name__ == "__main__":
    print("Part 1 example:", part_one(example_entries, 1000))
    print("Part 1 entry:", part_one(entries, 1000))

    print("Part 2 example:", part_two(example_entries))
    #print("Part 2 entry:", part_two(entries))
