from pathlib import Path
import os
import copy
from typing import List, Dict, Tuple
import re
import random
import sys

entry_file = Path(os.path.abspath(__file__)).parent / "entry.txt"
example_file = Path(os.path.abspath(__file__)).parent / "example.txt"

with entry_file.open("r") as f:
    entries = f.readlines()

for i in range(len(entries)):
    if entries[i][-1] == '\n':
        entries[i] = entries[i][:-1]

def dijsktra(nodes: set["Node"], start: "Node", end: "Node") -> List["Node"]:
    if start == end:
        return []

    dist = {n: sys.maxsize for n in nodes}
    dist[start] = 0
    prev = {n: None for n in nodes}
    seen = set()
    all_nodes: List[Node] = sorted(list(nodes), key=lambda x: dist[x], reverse=True)

    while len(all_nodes) > 0:
        curr: Node = all_nodes.pop()
        if end is not None and curr == end:
            break

        seen.add(curr)

        update = False

        for neighbor in curr.neighbors:
            if neighbor in seen:
                continue

            new_dist = dist[curr] + 1
            if new_dist < dist[neighbor]:
                dist[neighbor] = new_dist
                prev[neighbor] = curr
                update = True

        if update:
            all_nodes.sort(key=lambda x: dist[x], reverse=True)


    if prev[end] is not None:
        res = [end]
        curr = end
        while curr != start:
            res.append(prev[curr])
            curr = prev[curr]
        return res

    return []


class Node:
    def __init__(self, name: str, flow_rate: int):
        self.flow_rate = flow_rate
        self.name = name
        self.neighbors: set[Node]= set()
        self.paths_to_others: Dict[Node, List[Node]] = {}

        self.is_opening = False
        self.opened = False

    def add_neighbor(self, other: "Node"):
        self.neighbors.add(other)
        other.neighbors.add(self)

    def __hash__(self) -> int:
        return hash(self.name)

    def __eq__(self, other: "Node") -> bool:
        return other.name == self.name
    
    def __ne__(self, other: "Node") -> bool:
        return other.name != self.name

    def __repr__(self) -> str:
        return self.name

    def to_string(self) -> str:
        return f"Valve {self.name} has flow rate={self.flow_rate}; tunnels lead to valves " + ", ".join([n.name for n in self.neighbors])

    def distance_to(self, other: "Node"):
        if other == self:
            return 1
        
        return len(self.paths_to_others[other])

    def find_all_shortest_path_to_others(self, all_nodes: set["Node"]):
        for n in all_nodes:
            if n == self:
                continue

            self.paths_to_others[n] = dijsktra(all_nodes, self, n)


def parse_input(input: List[str]) -> set[Node]:
    pattern = "Valve ([A-Z]{2}) has flow rate=([0-9]+); tunnel(?:s)? lead(?:s)? to valve(?:s)? (.*)"
    res: set[Node] = set()
    for e in input:
        m = re.match(pattern, e)
        node = Node(m.group(1), int(m.group(2)))
        res.add(node)
        for neighbor in m.group(3).split(", "):
            for n in res:
                if n.name == neighbor:
                    node.add_neighbor(n)

    for n in res:
        n.find_all_shortest_path_to_others(res)

    return res


# Get all candidates that are not yet opened, sorted by their value (best in first place)
def get_candidates(current: Node, nodes_to_open: List[Node], minutes: int):
    all_candidates = []
    for candidate in nodes_to_open:
        if candidate == current \
            or candidate.flow_rate == 0 \
            or candidate.opened \
            or candidate.is_opening:
            continue

        distance = current.distance_to(candidate)
        if minutes - distance <= 0:
            continue

        value = (minutes - distance) * candidate.flow_rate
        all_candidates.append((candidate, value))

    return all_candidates
    #return sorted(all_candidates, key=lambda x: x[1], reverse=True)


def simulation(start: Node, nodes: set[Node], minutes: int, nodes_to_open: List[Node],current_flow_rate: int) -> Tuple[int, List[str]]:
    best_estimate = -1

    if len(nodes_to_open) == 0:
        return minutes * current_flow_rate, [start.name]

    # Find the non opened valve that has the best potential
    all_candidates = get_candidates(start, nodes, minutes)

    if len(all_candidates) == 0:
        return minutes * current_flow_rate, [start.name]

    best_candidates = None

    for candidate, value in all_candidates:
        travel_time = start.distance_to(candidate)

        assert travel_time > 0

        new_total = current_flow_rate * travel_time
        new_minutes = minutes - travel_time

        candidate.opened = True
        nodes_to_open.remove(candidate)
        estimate, next_best_candidates = simulation(candidate, nodes, new_minutes, nodes_to_open, current_flow_rate + candidate.flow_rate)
        nodes_to_open.add(candidate)
        candidate.opened = False

        new_total += estimate
        if new_total > best_estimate:
            best_estimate = new_total
            best_candidates = next_best_candidates

    return best_estimate, [start.name] + best_candidates


class Character:
    def __init__(self, id: int, start_node: Node):
        self.id = id
        self.current = start_node
        self.path: List[Node] = []
        self.is_opening = False
        self.direction: Node = None

        self.previous_states: List[Tuple[bool, Node]] = []

    # Return the change in flow rate
    def step(self) -> int:
        if self.is_opening:
            assert self.current.is_opening and not self.current.opened
            self.current.is_opening = False
            self.current.opened = True
            self.is_opening = False
            self.previous_states.append((True, None))
            self.direction = None
            return self.current.flow_rate

        if len(self.path) != 0:
            next_node = self.path.pop()
            assert (next_node in self.current.neighbors) and (next_node != self.current)
            self.previous_states.append((False, self.current))
            self.current = next_node
            if len(self.path) == 0:
                self.is_opening = True
                self.current.is_opening = True
            return 0

        assert False
        return 0

    # Return the change in flow rate
    def backtrack(self) -> int:
        assert len(self.previous_states) > 0
        opened_changed, previous_node = self.previous_states.pop()
        if not opened_changed:
            self.path.append(self.current)
            self.current.is_opening = False
            self.is_opening = False
            self.current = previous_node
            return 0
        else:
            self.path.clear()
            self.is_opening = True
            self.current.is_opening = True
            self.current.opened = False
            self.direction = self.current
            return -self.current.flow_rate

    def update_path(self, path: List[Node]):
        if path[-1] == self.current:
            self.path = list(path[:-1])
        else:
            self.path = list(path)

        assert len(self.path) > 0
        self.direction = self.path[0]

    def is_done(self):
        return len(self.path) == 0 and not self.is_opening

    def __repr__(self) -> str:
        return f"Character {self.id}: curr = {self.current}, path = {self.path}, direction = {self.direction}, is_opening = {self.is_opening}"


def test_character(start_node: Node):
    character = Character(0, start_node)

    print(character)

    all_nodes = list(start_node.paths_to_others.keys())

    first_target = random.choice(all_nodes)
    random_path1 = start_node.paths_to_others[first_target]
    random_path2 = random_path1[0].paths_to_others[random.choice(all_nodes)]
    curr = start_node

    print("Updating path...")
    character.update_path(random_path1)
    print(character)
    while not character.step():
        print(f"  - {character} ; curr_opened = {character.current.opened}")

    print(f"  - {character} ; curr_opened = {character.current.opened}")
    print("Updating path...")
    character.update_path(random_path2)
    print(character)
    while not character.step():
        print(f"  - {character} ; curr_opened = {character.current.opened}")

    print(f"  - {character} ; curr_opened = {character.current.opened}")

    print("Backtracking")
    while len(character.previous_states) > 0:
        character.backtrack()
        print(f"  - {character} ; curr_opened = {character.current.opened}")


def simulation2(characters: List[Character], nodes: set[Node], minutes: int, nodes_to_open: set[Node], current_flow_rate: int):
    best_estimate = -1

    if len(nodes_to_open) == 0 and all(c.is_done() for c in characters):
        return minutes * current_flow_rate

    all_candidates = [[] for _ in range(len(characters))]
    max_candidates = -1

    has_decision_point = False

    for c in characters:
        if c.is_done():
            all_candidates[c.id] = get_candidates(c.current, nodes_to_open, minutes)
            has_decision_point = True
            max_candidates = max(len(all_candidates[c.id]), max_candidates)

    if not has_decision_point:
        for c in characters:
            c.step()
        
        res = current_flow_rate + simulation2(characters, nodes, minutes - 1, nodes_to_open, current_flow_rate)

        for c in characters:
            c.backtrack()

        return res

    indexes_to_check = [set(range(len(c))) for c in all_candidates]

    all_is_done = False
    new_flow_rate = current_flow_rate

    while not all_is_done:
        for c in characters:
            found_candidate = None
            for index in indexes_to_check:
                candidate = all_candidates[c.id][index]
                if not candidate.is_opening and not candidate.opened \
                    and not any((other.direction == candidate for other in characters if other != c)):
                    found_candidate = candidate
                    indexes_to_check.remove(index)

            if found_candidate is not None:
                c.update_path(c.current.paths_to_others[found_candidate])

            new_flow_rate += c.step()

        estimate = current_flow_rate + simulation2(characters, nodes, minutes - 1, nodes_to_open, new_flow_rate)

    for i in range(max_candidates):
        for c in characters:
            if i >= len(all_candidates[c.id]):
                # Nothing to do
                c.step()
                continue


def solve(input: List[str], minutes: int):
    nodes = parse_input(input)

    nodes_to_open = [n for n in nodes if n.flow_rate > 0]

    start_node = None
    for n in nodes:
        if n.name == "AA":
            start_node = n
            break
    res, best_candidates = simulation(start_node, nodes, minutes, nodes_to_open, 0)
    return res


if __name__ == "__main__":
    print(solve(entries, 30))