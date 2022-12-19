from pathlib import Path
import os
import copy
from typing import List, Tuple, Dict, Any
import re
from collections import namedtuple

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


class Resources:
    def __init__(self, ore: int = 0, clay: int = 0, obsidian: int = 0, geode: int = 0):
        self.ore = ore
        self.clay = clay
        self.obsidian = obsidian
        self.geode = geode

    def __add__(self, other: "Resources") -> "Resources":
        return Resources(self.ore + other.ore, self.clay + other.clay, self.obsidian + other.obsidian, self.geode + other.geode)

    def __sub__(self, other: "Resources") -> "Resources":
        res = Resources(self.ore - other.ore, self.clay - other.clay, self.obsidian - other.obsidian, self.geode - other.geode)
        assert res.ore >= 0 and res.clay >= 0 and res.obsidian >= 0 and res.geode >= 0
        return res

    def __iadd__(self, other: "Resources") -> "Resources":
        self.ore += other.ore
        self.clay += other.clay
        self.obsidian += other.obsidian
        self.geode += other.geode
        
        return self

    def __isub__(self, other: "Resources") -> "Resources":
        self.ore -= other.ore
        self.clay -= other.clay
        self.obsidian -= other.obsidian
        self.geode -= other.geode

        assert self.ore >= 0 and self.clay >= 0 and self.obsidian >= 0 and self.geode >= 0

        return self

    def __ge__(self, other: "Resources") -> bool:
        # No need to test geode
        return self.ore >= other.ore and self.clay >= other.clay and self.obsidian >= other.obsidian

    def __repr__(self) -> str:
        return str((self.ore, self.clay, self.obsidian, self.geode))

    def __eq__(self, other: "Resources") -> bool:
        return self.ore == other.ore and self.clay == other.clay and self.obsidian == other.obsidian and self.geode == other.geode

    def __hash__(self) -> int:
        return hash((self.ore, self.clay, self.obsidian, self.geode))

    def __getitem__(self, index) -> int:
        return (self.ore, self.clay, self.obsidian, self.geode)[index]


class Blueprint:
    def __init__(self, id: int, ore_robot_cost: Resources, clay_robot_cost: Resources, obsidian_robot_cost: Resources, geode_robot_cost: Resources):
        self.id = id
        self.ore_robot_cost = ore_robot_cost
        self.clay_robot_cost = clay_robot_cost
        self.obsidian_robot_cost = obsidian_robot_cost
        self.geode_robot_cost = geode_robot_cost

        # The max number of each resources ever needed.
        # The number of robots cannot exceed this limit.
        self.max_ore = max((self.clay_robot_cost.ore, self.obsidian_robot_cost.ore, self.geode_robot_cost.ore))
        self.max_clay = self.obsidian_robot_cost.clay
        self.max_obsidian = self.geode_robot_cost.obsidian

    # Prepare a cache with all possible minutes, to avoid computing the 
    # multiplication at each steap
    def set_max_minutes(self, minutes):
        self.max_ore_cache = [m * self.max_ore for m in range(minutes+1)]
        self.max_clay_cache = [m * self.max_clay for m in range(minutes+1)]
        self.max_obsidian_cache = [m * self.max_obsidian for m in range(minutes+1)]

    # We have enough resource if have as many robots as our max number of resources
    # or we have enough resources to construct the machine that cost the most at every step
    # for the remaining number of minutes
    def has_enough_ore(self, robot: "Resources", res: "Resources", minutes: int) -> bool:
        return robot.ore >= self.max_ore or res.ore >= self.max_ore_cache[minutes]

    def has_enough_clay(self, robot: "Resources", res: "Resources", minutes: int) -> bool:
        return robot.clay >= self.max_clay or res.clay >= self.max_clay_cache[minutes]

    def has_enough_obsidian(self, robot: "Resources", res: "Resources", minutes: int) -> bool:
        return robot.obsidian >= self.max_obsidian or res.obsidian >= self.max_obsidian_cache[minutes]

    # We can construct the resource if we don't have enough of it, and we can pay its cost.
    def can_construct_ore(self, robot: "Resources", res: "Resources", minutes: int) -> bool:
        return not self.has_enough_ore(robot, res, minutes) and res.ore >= self.ore_robot_cost.ore

    def can_construct_clay(self, robot: "Resources", res: "Resources", minutes: int) -> bool:
        return not self.has_enough_clay(robot, res, minutes) and res.ore >= self.clay_robot_cost.ore

    def can_construct_obsidian(self, robot: "Resources", res: "Resources", minutes: int) -> bool:
        return not self.has_enough_obsidian(robot, res, minutes) and res.ore >= self.obsidian_robot_cost.ore and res.clay >= self.obsidian_robot_cost.clay

    # We cannot have enough of geode! We try to maximize it!
    def can_construct_geode(self, robot: "Resources", res: "Resources", minutes: int) -> bool:
        return res.ore >= self.geode_robot_cost.ore and res.obsidian >= self.geode_robot_cost.obsidian

    @staticmethod
    def from_input(input: str) -> "Blueprint":
        pattern = "Blueprint ([0-9]+): Each ore robot costs ([0-9]+) ore. Each clay robot costs ([0-9]+) ore. " \
        "Each obsidian robot costs ([0-9]+) ore and ([0-9]+) clay. Each geode robot costs ([0-9]+) ore and ([0-9]+) obsidian."

        m = re.match(pattern, input)
        if m is not None:
            id = int(m.group(1))
            ore_robot_cost = Resources(ore=int(m.group(2)))
            clay_robot_cost = Resources(ore=int(m.group(3)))
            obsidian_robot_cost = Resources(ore=int(m.group(4)), clay=int(m.group(5)))
            geode_robot_cost = Resources(ore=int(m.group(6)), obsidian=int(m.group(7)))
            return Blueprint(id, ore_robot_cost, clay_robot_cost, obsidian_robot_cost, geode_robot_cost)

    def __repr__(self) -> str:
        return f"Blueprint {self.id}: Each ore robot costs {self.ore_robot_cost.ore} ore. "\
            f"Each clay robot costs {self.clay_robot_cost.ore} ore. " \
            f"Each obsidian robot costs {self.obsidian_robot_cost.ore} ore and {self.obsidian_robot_cost.clay} clay. "\
            f"Each geode robot costs {self.geode_robot_cost.ore} ore and {self.geode_robot_cost.obsidian} obsidian."


# Cache for the robot factory
new_robots = (
    Resources(geode=1),
    Resources(obsidian=1),
    Resources(clay=1),
    Resources(ore=1)
)

def simulation(blueprint: Blueprint, minutes: int) -> Tuple[int, int, Any]:
    blueprint.set_max_minutes(minutes)
    return simulation_impl(blueprint, minutes, Resources(), Resources(ore=1), (False,) * 4)

def simulation_impl(blueprint: Blueprint, minutes: int, resources: Resources = None, robots: Resources = None, ignored = None) -> Tuple[int, int, Any]:
    # If we ignored all of them or arrive at the end, we can early out.
    if all(ignored) or minutes == 1:
        return robots.geode * minutes, 1, robots

    count = 0

    discard_doing_nothing = False

    # If we decided to ignore one, don't try to construct it before constructing another one
    can_construct = (
        ignored[0] or blueprint.can_construct_geode(robots, resources, minutes),
        ignored[1] or blueprint.can_construct_obsidian(robots, resources, minutes),
        ignored[2] or blueprint.can_construct_clay(robots, resources, minutes),
        ignored[3] or blueprint.can_construct_ore(robots, resources, minutes),
    )

    costs = (
        blueprint.geode_robot_cost,
        blueprint.obsidian_robot_cost,
        blueprint.clay_robot_cost,
        blueprint.ore_robot_cost
    )

    best = -1
    best_robots = robots

    # Try to make robots in priority order
    new_resources = resources + robots
    for i, (can_construct_robot, cost, new_robot, was_ignored) in enumerate(zip(can_construct, costs, new_robots, ignored)):
        if can_construct_robot and not was_ignored:
            final_resources = new_resources - cost
            res, incr, final_robots = simulation_impl(blueprint, minutes-1, final_resources, robots + new_robot, (False,) * 4)
            count += incr
            if res > best:
                best = res
                best_robots = final_robots
        
            # If I can construct a geode, no need to check others
            if i == 0:
                discard_doing_nothing = True

    if not discard_doing_nothing:
        res, incr, final_robots = simulation_impl(blueprint, minutes-1, new_resources, robots, can_construct)
        count += incr
        if res > best:
            best = res
            best_robots = final_robots

    res = robots.geode + best
    return res, count, best_robots


def solve(entries: List[str]):
    blueprints = [Blueprint.from_input(e) for e in entries]

    res = 0

    for bp in blueprints:
        nb_geodes, branches, robots = simulation(bp, 24)
        print(f"Blueprint {bp.id} has gather {nb_geodes} for a quality level of {bp.id * nb_geodes} with {branches} branches. Final robots: {robots}")
        res += bp.id * nb_geodes

    print("Part 1: Res =", res)

def solve2(entries: List[str]):
    blueprints = [Blueprint.from_input(e) for e in entries[:3]]

    res = 1

    for bp in blueprints:
        nb_geodes, branches, robots = simulation(bp, 32)
        print(f"Blueprint {bp.id} has gather {nb_geodes} with {branches} branches. Final robots: {robots}")
        res *= nb_geodes

    print("Part 2: Res =", res)

if __name__ == "__main__":
    solve(entries)
    solve2(entries)