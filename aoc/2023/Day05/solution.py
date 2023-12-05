from pathlib import Path
import os
import copy
from typing import List, Tuple, Dict
from aoc.common.parse_entry import parse_all
from aoc.common.utils import profile

entries, example_entries = parse_all(__file__, "entry.txt", "example.txt")


class Range:
    def __init__(self, _min: int, _range: int):
        assert(_range > 0)
        self.min = _min
        self.max = _min + _range

    def __contains__(self, x: int):
        return self.min <= x < self.max
    
    def __repr__(self) -> str:
        return f"[{self.min}; {self.max}]"


class SingleMap:
    def __init__(self, min_dest: int, min_source: int, _range: int):
        self.dest = Range(min_dest, _range)
        self.source = Range(min_source, _range)

    def __call__(self, x: int) -> Tuple[int, bool]:
        if x not in self.source:
            return x, False
        
        offset = x - self.source.min
        return self.dest.min + offset, True
    
    def reverse_call(self, x: int) -> Tuple[int, bool]:
        if x not in self.dest:
            return x, False
        
        offset = x - self.dest.min
        return self.source.min + offset, True
    
    @staticmethod
    def construct(entry: str) -> "SingleMap":
        return SingleMap(*map(int, entry.split()))
    
    def __repr__(self) -> str:
        return f"{self.dest} <- {self.source}"
    

class Map:
    def __init__(self, single_maps: List[SingleMap]) -> None:
        self.single_maps = single_maps

    def __call__(self, x: int) -> int:
        final_x = x
        for single_map in self.single_maps:
            temp, mapped = single_map(x)
            if mapped:
                final_x = temp
                break
        
        return final_x
    
    def reverse_call(self, x: int) -> int:
        final_x = x
        for single_map in self.single_maps:
            temp, mapped = single_map.reverse_call(x)
            if mapped:
                final_x = temp
                break
        
        return final_x
    
    @staticmethod
    def construct(entry: List[str]) -> "Map":
        return Map([SingleMap.construct(x) for x in entry])
    
    def __repr__(self) -> str:
        return str(self.single_maps)


class Almanac:
    def __init__(self, entry: List[str]):
        self.seeds = list(map(int, entry[0][7:].split()))

        self.seed_ranges = [Range(self.seeds[2 * i], self.seeds[2 * i+1]) for i in range(len(self.seeds) // 2)]

        self.maps: Dict[str, Map] = {}
        i = 2
        while i < len(entry):
            map_name = entry[i][:-1]
            i += 1
            start = i
            while i < len(entry) and len(entry[i]) > 0:
                i += 1

            self.maps[map_name] = Map.construct(entry[start:i])
            i += 1

    def __repr__(self) -> str:
        res = f"seeds: {self.seeds}\n"
        for map_name, maps in self.maps.items():
            res += f"{map_name}: {maps}\n"
        return res
    
    def map_seeds(self) -> List[str]:
        res = copy.deepcopy(self.seeds)
        for _map in self.maps.values():
            for i in range(len(res)):
                res[i] = _map(res[i])

        return res
    
    def reverse(self, x: int) -> bool:
        temp = x
        for _map in reversed(self.maps.values()):
            temp = _map.reverse_call(temp)

        return any([temp in seed for seed in self.seed_ranges])


def part_one(almanac: Almanac) -> int:
    return min(almanac.map_seeds())

#@profile
def part_two(almanac: Almanac) -> int:
    location = 1
    while True:
        if almanac.reverse(location):
            return location
        location += 1


if __name__ == "__main__":
    example_almanac = Almanac(example_entries)
    almanac = Almanac(entries)

    print("Part 1 example:", part_one(example_almanac))
    print("Part 1 entry:", part_one(almanac))

    print("Part 2 example:", part_two(example_almanac))
    print("Part 2 entry:", part_two(almanac))
