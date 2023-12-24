import copy
from typing import Any, List, Tuple, Dict, Optional, Set
from aoc.common.parse_entry import parse_all
from aoc.common.utils import profile
from aoc.common.grid import Grid
from aoc.common.point import Point
from aoc.common.direction import *

entries, example_entries = parse_all(__file__, "entry.txt", "example.txt")

class Tile:
    def __init__(self, c: str, slip: bool) -> None:
        self.walkable = c != "#"
        self.direction = None
        if self.walkable:
            if slip:
                if c == ">":
                    self.direction = Direction.East
                elif c == "v":
                    self.direction = Direction.South

class Map(Grid):
    def __init__(self, grid: List[str], slip: bool) -> None:
        super().__init__([[Tile(c, slip) for c in e] for e in grid])

class Node:
    def __init__(self, index: int, pos: Point):
        self.pos = pos
        self.edges: List[Edge] = []
        self.index = index

    def add_edge(self, edge: "Edge"):
        assert(edge.start == self.pos or edge.end == self.pos)
        if edge.one_way and edge.end == self.pos:
            return
        
        self.edges.append(edge)

    def __eq__(self, other) -> bool:
        if type(other) == Point:
            return self.pos == other
        
        return self.pos == other.pos
    
    def __hash__(self) -> int:
        return hash(self.pos)

class Edge:
    def __init__(self, index: int, start: Point, end: Point, cost: int, one_way: bool):
        self.start = start
        self.end = end
        self.cost = cost
        self.one_way = one_way
        self.index = index

    def get_next(self, pos: Point) -> Optional[Point]:
        if pos == self.start:
            return self.end
        
        if self.one_way:
            return None
        
        return self.start
        
class Graph:
    def __init__(self):
        self.nodes: Dict[Point, Node] = {}
        self.edges: List[Edge] = []
        self.start_point = None
        self.end_point = None

    @staticmethod
    def construct(entry: List[str], slip: bool) -> "Graph":
        map = Map(entry, slip)
        graph = Graph()
        for i, tile in enumerate(map.grid[0]):
            if tile.walkable:
                graph.start_point = Point(0, i)

        for i, tile in enumerate(map.grid[-1]):
            if tile.walkable:
                graph.end_point = Point(map.max_x - 1, i)

        stack = [(graph.start_point, Direction.South)]
        while len(stack) > 0:
            curr, dir = stack.pop()
            reverse_dir = turn_clockwise(dir, 180)
            if curr not in graph.nodes:
                graph.nodes[curr] = Node(len(graph.nodes), curr)

            for next_dir in [Direction.East, Direction.West, Direction.North, Direction.South]:
                # Can't go back
                if next_dir == reverse_dir:
                    continue

                one_way = False
                wrong_way = False

                steps = 1

                current_pos = advance(curr, next_dir)
                if not map.is_valid(current_pos) or not map[current_pos].walkable:
                    continue

                while True:
                    # Find next dir
                    next_reverse_dir = turn_clockwise(next_dir, 180)
                    tentative = [(advance(current_pos, d), d) for d in [Direction.East, Direction.West, Direction.North, Direction.South] if d != next_reverse_dir]
                    tentative = [x for x in tentative if map.is_valid(x[0]) and map[x[0]].walkable]

                    if len(tentative) == 1:
                        current_pos = tentative[0][0]
                        next_dir = tentative[0][1]

                        if map[current_pos].direction is not None:
                            assert(not one_way)
                            one_way = True
                            wrong_way = next_dir != map[current_pos].direction
                        
                        steps += 1
                        continue
                    
                    # We reached an intersection or the end
                    should_continue = False
                    if current_pos not in graph.nodes:
                        graph.nodes[current_pos] = Node(len(graph.nodes), current_pos)
                        should_continue = True

                    start_node = graph.nodes[current_pos] if wrong_way else graph.nodes[curr]
                    end_node = graph.nodes[current_pos] if not wrong_way else graph.nodes[curr]

                    # check if the edge already exist
                    edge_exist = False
                    for edge in graph.edges:
                        if (edge.start == current_pos and edge.end == curr) or (edge.start == curr and edge.end == current_pos):
                            edge_exist = True
                            break

                    if edge_exist:
                        break

                    graph.edges.append(Edge(len(graph.edges), start_node.pos, end_node.pos, steps, one_way))

                    start_node.add_edge(graph.edges[-1])
                    if not one_way:
                        end_node.add_edge(graph.edges[-1])

                    if should_continue:
                        stack.extend([(current_pos, x[1]) for x in tentative])
                    break

        return graph
    
    def find_max_length(self):
        seen_edges = [False] * len(self.edges)
        seen_nodes = [False] * len(self.nodes)
        self.current_max_length = 0

        return self.__find_max_length_internal(self.start_point, 0, seen_edges, seen_nodes)
    
    def __find_max_length_internal(self, curr: Point, curr_length, seen_edges, seen_nodes) -> int:
        if curr == self.end_point:
            if curr_length > self.current_max_length:
                self.current_max_length = curr_length
                print(self.current_max_length)
            return curr_length
        
        curr_node = self.nodes[curr]
        if seen_nodes[curr_node.index]:
            return None
        
        seen_nodes[curr_node.index] = True

        max_length = None

        for edge in self.nodes[curr].edges:
            if seen_edges[edge.index]:
                continue

            next_pos = edge.get_next(curr)
            if next_pos is not None:
                seen_edges[edge.index] = True
                length = self.__find_max_length_internal(next_pos, curr_length + edge.cost, seen_edges, seen_nodes)
                if length is not None and (max_length is None or length > max_length):
                    max_length = length
                seen_edges[edge.index] = False
        
        seen_nodes[curr_node.index] = False
        return max_length

@profile
def part_one(entry: List[str]) -> int:
    graph = Graph.construct(entry, True)
    return graph.find_max_length()

@profile
def part_two(entry: List[str]) -> int:
    graph = Graph.construct(entry, False)
    return graph.find_max_length()


if __name__ == "__main__":
    print("Part 1 example:", part_one(example_entries))
    print("Part 1 entry:", part_one(entries))

    print("Part 2 example:", part_two(example_entries))
    print("Part 2 entry:", part_two(entries))
