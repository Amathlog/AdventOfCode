from pathlib import Path
import os
import copy
from typing import List, Optional, Set, Tuple
from enum import IntEnum
from collections import defaultdict

entry_file = Path(os.path.abspath(__file__)).parent / "entry.txt"
entry2_file = Path(os.path.abspath(__file__)).parent / "entry2.txt"
example_file = Path(os.path.abspath(__file__)).parent / "example.txt"
example2_file = Path(os.path.abspath(__file__)).parent / "example2.txt"

with entry_file.open("r") as f:
    entries1 = f.readlines()

for i in range(len(entries1)):
    if entries1[i][-1] == '\n':
        entries1[i] = entries1[i][:-1]

with entry2_file.open("r") as f:
    entries2 = f.readlines()

for i in range(len(entries2)):
    if entries2[i][-1] == '\n':
        entries2[i] = entries2[i][:-1]


class Amphipod:
    def __init__(self, type: str, curr_pos: int, depth: int):
        self.type = type
        self.position = curr_pos
        self.depth = depth

        self.my_room = ord(self.type) - ord('A')
        self.my_room_position = (self.my_room + 1) * 2
        self.cost = 10 ** self.my_room

    def __repr__(self) -> str:
        return f"{self.type}, {self.position}"

    @property
    def state(self):
        return (self.type, self.position, self.depth)


class Table:
    def __init__(self, e: List[str]):
        self.rooms = [[Amphipod(e[j][i], (i + 1) * 2, j) for j in range(len(e) - 1, -1, -1)] for i in range(len(e[0]))]

        self.outside_spaces = {0: None, 1: None, 3: None, 5: None, 7: None, 9: None, 10: None}
        self.depth = len(self.rooms[0])

    @property
    def state(self):
        room_states = []
        for r in self.rooms:
            room_states += [v.state for v in r]
        return tuple([v.state for v in self.outside_spaces.values() if v is not None] + room_states)

    def get_valid_moves(self, amphipod: Amphipod):
        my_position = amphipod.position

        if my_position in self.outside_spaces:
            # We are outside, we need to check if we can move back to our room
            # First rule: Can't go back in our room if there are other types than mine
            if not self.is_same_than_me(amphipod):
                return []

            # Check if there is a path to our room
            our_room_position = amphipod.my_room_position

            min_pos = min(my_position, our_room_position)
            max_pos = max(my_position, our_room_position)

            for p in range(min_pos, max_pos + 1):
                if p not in self.outside_spaces or p == my_position:
                    continue
                if self.outside_spaces[p] is not None:
                    return []

            # There is a path!
            return [(my_position, our_room_position)]

        # We are in a room, we can move outside or in our room (is there is space)
        # But if we already are in the right room, we only move if there is other types in this room
        if my_position == amphipod.my_room_position and self.is_same_than_me(amphipod):
            return []

        res = []

        # To move outside, we can only move if the others spaces are not occupied
        left_pos = my_position - 1
        right_pos = my_position + 1
        left_done = False
        right_done = False

        while left_pos >= 0 or right_pos <= 10:
            if not left_done and left_pos in self.outside_spaces:
                if self.outside_spaces[left_pos] is None:
                    res.append((my_position, left_pos))
                else:
                    left_done = True
            elif not left_done and left_pos == amphipod.my_room_position and self.is_same_than_me(amphipod):
                # We have a path from our current room to the right room.
                # It's the best thing to do
                return [(my_position, left_pos)]

            if not right_done and right_pos in self.outside_spaces:
                if self.outside_spaces[right_pos] is None:
                    res.append((my_position, right_pos))
                else:
                    right_done = True
            elif not right_done and right_pos == amphipod.my_room_position and self.is_same_than_me(amphipod):
                # We have a path from our current room to the right room.
                # It's the best thing to do
                return [(my_position, right_pos)]

            left_pos -= 1
            right_pos += 1

        return res

    def get_all_valid_moves(self):
        res = []
        for a in self.outside_spaces.values():
            if a is not None:
                res.extend(self.get_valid_moves(a))
        
        for r in self.rooms:
            if len(r) > 0:
                res.extend(self.get_valid_moves(r[-1]))

        return res

    def is_same_than_me(self, amphipod: Amphipod):
        for x in self.rooms[amphipod.my_room]:
            if x.type != amphipod.type:
                return False

        return True

    # Move and return the cost
    def move(self, moves: Tuple[int, int], is_undo: bool = False) -> int:
        curr_pos, new_pos = moves
        latteral_move_cost = abs(new_pos - curr_pos)
        if curr_pos in self.outside_spaces:
            # assert(curr_pos in self.outside_spaces)
            amphipod = self.outside_spaces[curr_pos]
            # assert(amphipod is not None)
            self.outside_spaces[curr_pos] = None

            room_number = new_pos // 2 - 1
            # In case of undo, we can move into a room that is not ours.
            # But not in a normal move, so check that too
            # assert(is_undo or room_number == amphipod.my_room)
            # assert(len(self.rooms[room_number]) < self.depth)


            self.rooms[room_number].append(amphipod)
            amphipod.depth = self.depth - len(self.rooms[room_number])
            nb_moves = latteral_move_cost + amphipod.depth + 1
            # assert(is_undo or new_pos == amphipod.my_room_position)
        elif new_pos in self.outside_spaces:
            # If we go outside, we have to be in a room, so check that
            # assert(curr_pos % 2 == 0)
            room_number = curr_pos // 2 - 1
            # assert(len(self.rooms[room_number]) != 0)
            amphipod = self.rooms[room_number].pop()
            # assert(new_pos in self.outside_spaces)
            # assert(self.outside_spaces[new_pos] is None)
            self.outside_spaces[new_pos] = amphipod
            nb_moves = latteral_move_cost + amphipod.depth + 1
            amphipod.depth = -1
        else:
            # If we move from a room to another one, the other room needs to be our room (if it is not undo)
            # assert(curr_pos % 2 == 0)
            # assert(new_pos % 2 == 0)
            curr_room_number = curr_pos // 2 - 1
            new_room_number = new_pos // 2 - 1
            # assert(len(self.rooms[curr_room_number]) != 0)
            amphipod = self.rooms[curr_room_number].pop()
            # assert(is_undo or new_room_number == amphipod.my_room)
            # assert(len(self.rooms[new_room_number]) < self.depth)
            # Compute the cost to go outside the room
            nb_moves = amphipod.depth + 1   
            self.rooms[new_room_number].append(amphipod)
            amphipod.depth = self.depth - len(self.rooms[new_room_number])
            # Add the latteral move + the cost to go inside the room
            nb_moves += latteral_move_cost + amphipod.depth + 1

        amphipod.position = new_pos
        return amphipod.cost * nb_moves

    # Undo the move, return the inverse of the cost
    def undo(self, moves: Tuple[int, int]):
        return -self.move((moves[1], moves[0]), True)

    def is_room_OK(self, room_number):
        room = self.rooms[room_number]
        if len(room) < self.depth:
            return False

        for a in room:
            if room_number != a.my_room:
                return False

        return True

    def is_solved(self):
        for e in self.outside_spaces.values():
            if e is not None:
                return False

        for i in range(len(self.rooms)):
            if not self.is_room_OK(i):
                return False

        return True

    def __repr__(self) -> str:
        width = (len(self.rooms) + 2) * 2 + 1
        res = "#" * width + "\n"
        res += "#"
        for outside in range(width - 2):
            if outside not in self.outside_spaces or self.outside_spaces[outside] is None:
                res += "."
            else:
                res += self.outside_spaces[outside].type
        res += "#\n"
        for i in range(self.depth):
            res += "###" if i == 0 else "  #"
            for r in self.rooms:
                index = self.depth - len(r) - 1 - i
                res += ".#" if index >= 0 else r[index].type + "#"

            res += "##\n" if i == 0 else "# \n"

        res += "  " + "#" * (len(self.rooms) * 2 + 1) + "  \n"

        return res


class Moves:
    def __init__(self, moves, cost):
        self.moves = copy.deepcopy(moves)
        self.cost = cost

def solve(table: Table, cache: Optional[Set] = None, current_moves: Moves = None, best_moves: Moves = None) -> Moves:
    # if cache is None:
    #     cache = set()

    if best_moves is None:
        best_moves = Moves([], -1)

    if current_moves is None:
        current_moves = Moves([], 0)

    # No need to continue if the current cost is higher than the current minimum
    # if best_moves.cost != -1 and current_moves.cost > best_moves.cost:
    #     return best_moves

    if table.is_solved():
        if best_moves.cost == -1 or current_moves.cost < best_moves.cost:
            best_moves.moves = copy.deepcopy(current_moves.moves)
            best_moves.cost = current_moves.cost

        return best_moves

    # cache.add(table.state)

    moves = table.get_all_valid_moves()
    for m in moves:
        current_moves.moves.append(m)
        current_moves.cost += table.move(m)
        best_moves = solve(table, cache, current_moves, best_moves)
        current_moves.moves.pop()
        current_moves.cost += table.undo(m)

    return best_moves



if __name__ == "__main__":
    # table = Table(entries)
    # print(table.state)
    # total_cost = 0
    # for m in [(6, 3), (4, 6), (4, 5), (3, 4), (2, 4), (8, 7), (8, 9), (7, 8), (5, 8), (9, 2)]:
    #     print(table)
    #     cost = table.move(m)
    #     total_cost += cost
    #     print(cost)
    #     print(table.state)

    # print(table)
    # print(total_cost)

    # for i, entries in enumerate([entries1, entries2]):
    for i, entries in enumerate([entries2]):
        table = Table(entries)
        best_moves = solve(table)
        print(f"Answer {i+1}: {best_moves.cost}, {best_moves.moves}")

        new_table = Table(entries)
        for m in best_moves.moves:
            print(new_table)
            print(new_table.move(m))
        print(new_table)