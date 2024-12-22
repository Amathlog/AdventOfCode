import copy
from typing import List, Tuple, Dict, Optional, Set
from aoc.common.parse_entry import parse_all
from aoc.common.utils import profile
from aoc.common.point import Point, up, down, left, right
from aoc.common.astar import AStar_Solver

entries, example_entries = parse_all(__file__, "entry.txt", "example.txt")

keypad = {
    '7' : Point(0, 0),
    '8' : Point(0, 1),
    '9' : Point(0, 2),
    '4' : Point(1, 0),
    '5' : Point(1, 1),
    '6' : Point(1, 2),
    '1' : Point(2, 0),
    '2' : Point(2, 1),
    '3' : Point(2, 2),
    '0' : Point(3, 1),
    'A' : Point(3, 2)
}

dir_keypad = {
    '^' : Point(0, 1),
    'A' : Point(0, 2),
    '<' : Point(1, 0),
    'v' : Point(1, 1),
    '>' : Point(1, 2)
}

dir_map = {
    '^': up,
    'v': down,
    '<': left,
    '>': right
}

reverse_keypad = {v: k for k, v in keypad.items()}
reverse_dir_keypad = {v: k for k, v in dir_keypad.items()}
reverse_dir_map = {v: k for k, v in dir_map.items()}

class State3:
    def __init__(self, robot1: Point, robot2: Point, robot3: Point, code: str, is_start: bool = False):
        self.robot1 = robot1
        self.robot2 = robot2
        self.robot3 = robot3
        self.code = code
        self.is_start = is_start

    @staticmethod
    def init_state() -> "State":
        return State(dir_keypad['A'], dir_keypad['A'], keypad['A'], "", True)

    def __eq__(self, value):
        return self.robot1 == value.robot1 and self.robot2 == value.robot2 and self.robot3 == value.robot3 and self.code == value.code

    def __hash__(self):
        return hash((self.robot1, self.robot2, self.robot3, self.code))
    
    def get_neighbors(self, final_code: str):
        res = []
        # Activate
        robot_1_action = reverse_dir_keypad[self.robot1]
        if robot_1_action == 'A':
            robot_2_action = reverse_dir_keypad[self.robot2]
            if robot_2_action == 'A':
                robot_3_action = reverse_keypad[self.robot3]
                c = final_code[len(self.code)]
                if robot_3_action == c:
                    res.append(State(self.robot1, self.robot2, self.robot3, self.code + c))
            else:
                robot3_temp = self.robot3 + dir_map[robot_2_action]
                if robot3_temp in reverse_keypad:
                    res.append(State(self.robot1, self.robot2, robot3_temp, self.code))
        else:
            robot2_temp = self.robot2 + dir_map[robot_1_action]
            if robot2_temp in reverse_dir_keypad:
                res.append(State(self.robot1, robot2_temp, self.robot3, self.code))

        for dir in [up, left, right, down]:
            robot1_temp = self.robot1 + dir
            if robot1_temp in reverse_dir_keypad:
                res.append(State(robot1_temp, self.robot2, self.robot3, self.code))
        
        return res
    
class State:
    def __init__(self, robot1: Point, robot2: Point, robot3: Point, robot4: Point, code: str, is_start: bool = False):
        self.robot1 = robot1
        self.robot2 = robot2
        self.robot3 = robot3
        self.robot4 = robot4
        self.code = code
        self.is_start = is_start

    @staticmethod
    def init_state() -> "State":
        return State(dir_keypad['A'], dir_keypad['A'], dir_keypad['A'], keypad['A'], "", True)

    def __eq__(self, value):
        return self.robot1 == value.robot1 and self.robot2 == value.robot2 and self.robot3 == value.robot3 and self.robot4 == value.robot4 and self.code == value.code

    def __hash__(self):
        return hash((self.robot1, self.robot2, self.robot3, self.robot4, self.code))
    
    def get_neighbors(self, final_code: str):
        res = []
        # Activate
        robot_1_action = reverse_dir_keypad[self.robot1]
        if robot_1_action == 'A':
            robot_2_action = reverse_dir_keypad[self.robot2]
            if robot_2_action == 'A':
                robot_3_action = reverse_dir_keypad[self.robot3]
                if robot_3_action == 'A':
                    robot_4_action = reverse_keypad[self.robot4]
                    c = final_code[len(self.code)]
                    if robot_4_action == c:
                        res.append(State(self.robot1, self.robot2, self.robot3, self.robot4, self.code + c))
                else:
                    robot4_temp = self.robot4 + dir_map[robot_3_action]
                    if robot4_temp in reverse_keypad:
                        res.append(State(self.robot1, self.robot2, self.robot3, robot4_temp, self.code))
            else:
                robot3_temp = self.robot3 + dir_map[robot_2_action]
                if robot3_temp in reverse_dir_keypad:
                    res.append(State(self.robot1, self.robot2, robot3_temp, self.robot4, self.code))
        else:
            robot2_temp = self.robot2 + dir_map[robot_1_action]
            if robot2_temp in reverse_dir_keypad:
                res.append(State(self.robot1, robot2_temp, self.robot3, self.robot4, self.code))

        for dir in [up, left, right, down]:
            robot1_temp = self.robot1 + dir
            if robot1_temp in reverse_dir_keypad:
                res.append(State(robot1_temp, self.robot2, self.robot3, self.robot4, self.code))
        
        return res
    

class KeypadConundrum(AStar_Solver):
    def __init__(self, code: str):
        super().__init__()
        self.code = code

    def heuristic(self, state: State) -> int:
        return 0
    
    def get_cost(self, state: State) -> int:
        return 1
    
    def get_neighbors(self, state: State) -> List[Point]:
        return state.get_neighbors(self.code)
    
    def is_start(self, state: State) -> bool:
        return state.is_start
    
    def is_end(self, state: State) -> bool:
        return state.code == self.code
    
    def get_start_states(self) -> List[Point]:
        return [State.init_state()]


def print_path(path: List[State]):
    robot1_path = ""
    robot2_path = ""
    robot3_path = ""
    for i in range(len(path) - 1):
        curr = path[i]
        next = path[i+1]
        robot1_diff = next.robot1 - curr.robot1
        if robot1_diff != Point(0, 0):
            robot1_path += reverse_dir_map[robot1_diff]
            continue

        robot1_path += "A"
        robot2_diff = next.robot2 - curr.robot2
        if robot2_diff != Point(0, 0):
            robot2_path += reverse_dir_map[robot2_diff]
            continue

        robot2_path += "A"
        robot3_diff = next.robot3 - curr.robot3
        if robot3_diff != Point(0, 0):
            robot3_path += reverse_dir_map[robot3_diff]
            continue

        robot3_path += "A"
    
    print(robot1_path)
    print(robot2_path)
    print(robot3_path)
    print(path[-1].code)

@profile
def part_one(entry: List[str]) -> int:
    result = 0
    for e in entry:
        solver = KeypadConundrum(e)
        res = solver.solve()
        length = len(res) - 1
        # print_path(res)
        # print(length)
        # print()
        result += int(e[:-1]) * length
    return result

#################################################

def compute_shortest_paths(d):
    shortest_paths: Dict[str, Dict[str, List[str]]] = {}
    for start_c, start_pos in d.items():
        if start_c not in shortest_paths:
            shortest_paths[start_c] = {}
        for end_c, end_pos in d.items():
            if start_c == end_c:
                continue

            if end_c not in shortest_paths[start_c]:
                shortest_paths[start_c][end_c] = []

            diff = end_pos - start_pos
            priority = [right, up, down, left]
            for p in priority:
                dot_product = diff.dot(p)
                if dot_product > 0:
                    shortest_paths[start_c][end_c].extend([reverse_dir_map[p]] * dot_product)
    return shortest_paths

shortest_paths_dirs = compute_shortest_paths(dir_keypad)
shortest_paths_keys = compute_shortest_paths(keypad)
print(shortest_paths_keys)

@profile
def part_two(entry: List[str]) -> int:
    nb_robots = 3

    starting_pos = ["A"] * nb_robots


if __name__ == "__main__":
    # print("Part 1 example:", part_one(example_entries))
    # print("Part 1 entry:", part_one(entries))

    print("Part 2 example:", part_two(example_entries))
    print("Part 2 entry:", part_two(entries))
