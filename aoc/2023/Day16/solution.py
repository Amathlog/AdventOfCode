import copy
from typing import List, Tuple, Dict, Optional, Set
from aoc.common.parse_entry import parse_all
from aoc.common.utils import profile
from aoc.common.point import Point
from aoc.common.grid import Grid
from enum import IntEnum


entries, example_entries = parse_all(__file__, "entry.txt", "example.txt")

class Direction(IntEnum):
    Left = 0
    Down = 1
    Right = 2
    Up = 3

dir_to_incr = [Point(0, -1), Point(1, 0), Point(0, 1), Point(-1, 0)]

class Laser:
    def __init__(self, pos: Point, dir: Direction):
        self.pos = pos
        self.dir = dir

    def advance(self):
        self.pos += dir_to_incr[self.dir]
    
    def __eq__(self, other: "Laser") -> bool:
        return self.pos == other.pos and self.dir == other.dir
    
    def __hash__(self) -> int:
        return hash((self.pos, self.dir))

class Map(Grid):
    def __init__(self, grid: List[str]):
        super().__init__(grid)
        self.energized = Grid([[0 for _ in range(self.max_y)] for __ in range(self.max_x)])
        
    def next(self, laser: Laser, energize: bool = True) -> Tuple[Optional[Laser], Optional[Laser]]:
        if not self.is_valid(laser.pos):
            return (None, None)
        
        if energize:
            self.energized[laser.pos] = 1
        
        new_laser = Laser(laser.pos, laser.dir)

        new_laser2 = None

        c = self[new_laser.pos]
        if c == ".":
            pass
        elif c == "/":
            if new_laser.dir == Direction.Left or new_laser.dir == Direction.Down:
                new_laser.dir = Direction.Down if new_laser.dir == Direction.Left else Direction.Left
            else:
                new_laser.dir = Direction.Right if new_laser.dir == Direction.Up else Direction.Up
        elif c == "\\":
            if new_laser.dir == Direction.Left or new_laser.dir == Direction.Up:
                new_laser.dir = Direction.Up if new_laser.dir == Direction.Left else Direction.Left
            else:
                new_laser.dir = Direction.Right if new_laser.dir == Direction.Down else Direction.Down
        elif c == "-":
            if new_laser.dir == Direction.Left or new_laser.dir == Direction.Right:
                pass
            else:
                new_laser.dir = Direction.Left
                new_laser2 = Laser(new_laser.pos, Direction.Right)
        elif c == "|":
            if new_laser.dir == Direction.Up or new_laser.dir == Direction.Down:
                pass
            else:
                new_laser.dir = Direction.Up
                new_laser2 = Laser(new_laser.pos, Direction.Down)

        if new_laser2 is None:
            new_laser.advance()
        
        return new_laser, new_laser2
    
    def resolve(self, initial_pos: Point, initial_dir: Direction):
        lasers = [Laser(initial_pos, initial_dir)]
        seen_lasers = set()
        while len(lasers) > 0:
            laser = lasers.pop()
            if laser in seen_lasers:
                continue
            seen_lasers.add(laser)

            new_laser, new_laser2 = self.next(laser)
            if new_laser is not None:
                lasers.append(new_laser)
            if new_laser2 is not None:
                lasers.append(new_laser2)
        
        return sum([sum(e) for e in self.energized.grid])
    
    def resolve_max_recurse(self, laser: Laser, all_trajectories: Dict[Laser, Set[Point]], seen_lasers: Set[Laser] = None) -> List[Point]:
        if seen_lasers is None:
            seen_lasers = set()

        res = []

        curr = laser
        while True:
            if curr in seen_lasers or not self.is_valid(curr.pos):
                break
        
            if curr in all_trajectories:
                res.extend(all_trajectories[curr])
                break
        
            res.append(curr.pos)
            seen_lasers.add(laser)
            curr, new_laser = self.next(curr, energize=False)
            if curr is None:
                break

            if new_laser is not None and new_laser not in seen_lasers:
                res.extend(self.resolve_max_recurse(new_laser, all_trajectories, seen_lasers))
            
        if laser and (laser.pos.x == 0 or laser.pos.y == 0 or laser.pos.x == self.max_x - 1 or laser.pos.y == self.max_y - 1):
            all_trajectories[copy.deepcopy(laser)] = set(res)

        return res
    
    def resolve_max(self) -> int:
        all_trajectories: Dict[Laser, Set[Point]] = {}
        all_lasers = []
        max_energized = -1
        all_lasers.extend([Laser(Point(x, 0), Direction.Right) for x in range(self.max_x)])
        all_lasers.extend([Laser(Point(x, self.max_y - 1), Direction.Left) for x in range(self.max_x)])
        all_lasers.extend([Laser(Point(0, y), Direction.Down) for y in range(self.max_y)])
        all_lasers.extend([Laser(Point(self.max_x - 1, y), Direction.Up) for y in range(self.max_y)])

        for laser in all_lasers:
            self.resolve_max_recurse(laser, all_trajectories)
            max_energized = max(max_energized, len(all_trajectories[laser]))

        return max_energized

@profile
def part_one(entry: List[str]) -> int:
    my_map = Map(entry)
    return my_map.resolve(Point(0, 0), Direction.Right)

@profile
def part_two(entry: List[str]) -> int:
    my_map = Map(entry)
    return my_map.resolve_max()


if __name__ == "__main__":
    print("Part 1 example:", part_one(example_entries))
    print("Part 1 entry:", part_one(entries))

    print("Part 2 example:", part_two(example_entries))
    print("Part 2 entry:", part_two(entries))
