from pathlib import Path
import os
import copy
from typing import List, Optional, Tuple, Union

entry_file = Path(os.path.abspath(__file__)).parent / "entry.txt"
example_file = Path(os.path.abspath(__file__)).parent / "example.txt"

with entry_file.open("r") as f:
    entries = f.readlines()

for i in range(len(entries)):
    if entries[i][-1] == '\n':
        entries[i] = entries[i][:-1]

class Action:
    EXPLODE = 1
    SPLIT = 2
    def __init__(self, type: int, item: "Pair") -> None:
        self.type = type
        self.item = item

    def apply(self) -> List["Action"]:
        if self.type == Action.EXPLODE:
            return self.item.explode()
        
        return self.item[0].split(self.item[1])

    def get_item_id(self):
        if self.type == Action.EXPLODE:
            return self.item.id

        return self.item[0].id

    def __repr__(self) -> str:
        if self.type == Action.EXPLODE:
            return f"EXPLODE {{{self.item.id}}}: {self.item}"
        return f"SPLIT {{{self.item[0].id}}}: {self.item[0].left if self.item[1] else self.item[0].right}"

class Pair:
    def __init__(self, left: Union["Pair", int], right: Union["Pair", int], parent: Optional["Pair"] = None):
        self.left = left
        self.right = right
        self.parent = parent

    def magnitude(self):
        left_magnitude = self.left if type(self.left) is int else self.left.magnitude()
        right_magnitude = self.right if type(self.right) is int else self.right.magnitude()
        return left_magnitude * 3 + right_magnitude * 2

    @property
    def depth(self):
        return self.parent.depth + 1 if self.parent is not None else 0

    @property
    def id(self):
        if self.parent is None:
            return 0
        
        return self.parent.id * 2 + int(self.parent.right == self) + 1

    def find_left_right_most(self, is_left: bool) -> Tuple[Optional["Pair"], bool]:
        curr = self.parent
        previous = self
        while curr is not None:
            if (is_left and (previous == curr.left)) \
                or (not is_left and (previous == curr.right)):
                previous = curr
                curr = curr.parent
                continue
            break

        if curr is None:
            return None, False

        if (is_left and type(curr.left) is int) \
            or (not is_left and type(curr.right) is int):
            return curr, is_left

        curr = curr.left if is_left else curr.right
        # Reverse the direction
        while True:
            if (is_left and type(curr.right) is int) \
                or (not is_left and type(curr.left) is int):
                return curr, not is_left
            curr = curr.right if is_left else curr.left

    def explode(self) -> List[Action]:
        if self.depth < 4:
            # Already handled
            return []

        actions = []
        # Left part
        closest_left, is_left = self.find_left_right_most(True)
        if closest_left is not None:
            if is_left:
                closest_left.left += self.left
                if closest_left.left >= 10:
                    actions.append(Action(Action.SPLIT, (closest_left, is_left)))
            else:
                closest_left.right += self.left
                if closest_left.right >= 10:
                    actions.append(Action(Action.SPLIT, (closest_left, is_left)))

        # Right part
        closest_right, is_left = self.find_left_right_most(False)
        if closest_right is not None:
            if is_left:
                closest_right.left += self.right
                if closest_right.left >= 10:
                    actions.append(Action(Action.SPLIT, (closest_right, is_left)))
            else:
                closest_right.right += self.right
                if closest_right.right >= 10:
                    actions.append(Action(Action.SPLIT, (closest_right, is_left)))

        # Reduce
        if self.parent.left == self:
            self.parent.left = 0
        else:
            self.parent.right = 0

        return actions

    def split(self, is_left: bool) -> List[Action]:
        value = self.left if is_left else self.right
        if type(value) is Pair or value < 10:
            # Already handled
            return []

        value_left = value // 2
        value_right = value_left + 1 if value % 2 == 1 else value_left
        new_pair = Pair(value_left, value_right, self)
        if is_left:
            self.left = new_pair
        else:
            self.right = new_pair

        if new_pair.depth == 4:
            return [Action(Action.EXPLODE, new_pair)]

        return []

    def __repr__(self) -> str:
        return f"[{str(self.left)},{str(self.right)}]"

    def add(self, other: "Pair") -> "Pair":
        assert self.parent == None
        new_pair = Pair(self, other, None)
        self.parent = new_pair
        other.parent = new_pair
        return new_pair


def parse_pairs(line: str):
    stack = []
    for c in line:
        if c == "[":
            stack.append(Pair(None, None))
        elif c in [",", " "]:
            continue
        elif c == "]":
            close = stack.pop()
            if len(stack) > 0:
                if stack[-1].left is None:
                    stack[-1].left = close
                    close.parent = stack[-1]
                else:
                    stack[-1].right = close
                    close.parent = stack[-1]
            else:
                return close
        else:
            if stack[-1].left is None:
                stack[-1].left = int(c)
            else:
                stack[-1].right = int(c)

def scan_for_explosions(root: Pair) -> Action:
    to_search = [root]
    actions = None
    while len(to_search) > 0:
        curr = to_search.pop()
        if type(curr) is int:
            continue

        if curr.depth == 4:
            return Action(Action.EXPLODE, curr)

        to_search.extend([curr.right, curr.left])

    return actions

def scan_for_split(root: Pair) -> Action:
    to_search = [(None, root)]
    actions = None
    while len(to_search) > 0:
        parent, curr = to_search.pop()

        if type(curr) is int:
            if curr >= 10:
                return Action(Action.SPLIT, (parent, parent.left == curr))
            continue

        to_search.extend([(curr, curr.right), (curr, curr.left)])

    return actions

def add_two(left: Pair, right: Pair) -> Pair:
    temp = left.add(right)

    while True:
        action = scan_for_explosions(temp)
        if action is None:
            action = scan_for_split(temp)

        if action is None:
            break

        action.apply()

    return temp

if __name__ == "__main__":
    all_pairs = [parse_pairs(s) for s in entries]

    res = all_pairs[0]

    for other in all_pairs[1:]:
        res = add_two(res, other)

    print("First answer:", res.magnitude())

    all_pairs = [parse_pairs(s) for s in entries]
    max_value = 0
    for i in range(len(all_pairs)):
        for j in range(len(all_pairs)):
            if i == j:
                continue

            temp = add_two(all_pairs[i], all_pairs[j])
            value = temp.magnitude()
            if value > max_value:
                max_value = value

            # Reset the full pairs to avoid border effects
            all_pairs = [parse_pairs(s) for s in entries]

    print("Second answer:", max_value)