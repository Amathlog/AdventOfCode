from pathlib import Path
import os
import copy
from typing import List, Dict, Tuple
import re
import random
import sys
import itertools
import time
import numpy as np

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
        self.direction: Node = None
        self.distance_to_dir: int = 0
        self.current = start_node
    
    def step(self, nb_steps: int) -> bool:
        if self.distance_to_dir == sys.maxsize:
            return False

        assert nb_steps <= self.distance_to_dir
        self.distance_to_dir -= nb_steps
        if self.distance_to_dir == 0:
            self.current = self.direction
            self.direction = None

        return self.distance_to_dir == 0

    def backtrack(self, nb_steps: int):
        if self.distance_to_dir == sys.maxsize:
            return
    
        self.distance_to_dir += nb_steps


def simulation2(characters: List[Character], nodes: set[Node], minutes: int, nodes_to_open: set[Node], current_flow_rate: int):
    best_estimate = minutes * current_flow_rate

    if len(nodes_to_open) == 0 and all((c.direction is None for c in characters)):
        return minutes * current_flow_rate

    characters_to_update = [(c, c.current) for c in characters if c.distance_to_dir == 0]

    permutations = list(itertools.permutations(list(nodes_to_open), len(characters_to_update)))
    all_times = []

    ran_once = False
    start = None
    i = 0
    while not ran_once or i < len(permutations):
        if current_flow_rate == 0:
            if start is not None:
                all_times.append(time.perf_counter() - start)
            start = time.perf_counter()
            remaining_time = str(np.mean(all_times) * (len(permutations) - i)) if len(all_times) > 0 else "N/A"
            print(f"Computing permuatation {i} over {len(permutations)}. Estimated time remaining = {remaining_time}s")
        ran_once = True
        new_nodes_to_open = set(list(nodes_to_open))
        for index, (c, c_current) in enumerate(characters_to_update):
            if i < len(permutations):
                node = permutations[i][index]
                c.distance_to_dir = c_current.distance_to(node)
                if c.distance_to_dir > minutes:
                    c.distance_to_dir = sys.maxsize
                    c.direction = None
                else:
                    c.direction = node
                    new_nodes_to_open.remove(node)
            else:
                # Nothing else to do, don't contribute to next decision point
                c.distance_to_dir = sys.maxsize
                c.direction = None

        i += 1
        # Nothing left to do
        if all((c.direction is None for c in characters)):
            for c, _ in characters_to_update:
                c.distance_to_dir = 0
            continue
            
        nb_steps = min((c.distance_to_dir for c in characters))
        total = nb_steps * current_flow_rate

        current = {}
        for c in characters:
            current[c.id] = c.current
            if c.step(nb_steps):
                current_flow_rate += c.current.flow_rate
                c.current.opened = True

        estimated = simulation2(characters, nodes, minutes - nb_steps, new_nodes_to_open, current_flow_rate)

        if total + estimated > best_estimate:
            best_estimate = total + estimated

        for c in characters:
            if c.distance_to_dir == 0:
                current_flow_rate -= c.current.flow_rate
                c.current.opened = False
                c.direction = c.current
                c.current = current[c.id]

            c.backtrack(nb_steps)

    # need to make sure that characters that was updated are back to 0
    for c, _ in characters_to_update:
        c.distance_to_dir = 0

    return best_estimate


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

def solve2(input: List[str], minutes: int, nb_characters: int):
    nodes = parse_input(input)

    nodes_to_open = set([n for n in nodes if n.flow_rate > 0])

    start_node = None
    for n in nodes:
        if n.name == "AA":
            start_node = n
            break

    characters = [Character(i, start_node) for i in range(nb_characters)]

    res = simulation2(characters, nodes, minutes, nodes_to_open, 0)
    return res


if __name__ == "__main__":
    #print(solve(entries, 30))
    #print(solve2(entries, 30, 1))
    print(solve2(entries, 26, 2))