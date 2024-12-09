import copy
from typing import List, Tuple, Dict, Optional, Set
from aoc.common.parse_entry import parse_all
from aoc.common.utils import profile

entries, example_entries = parse_all(__file__, "entry.txt", "example.txt")

class Block:
    def __init__(self, id: int, size: int, prev: "Block"):
        self.id = id
        self.size = size
        self.prev = prev
        if prev is not None:
            prev.next = self
        self.next = None

    def is_free(self) -> bool:
        return self.id < 0
    
    def split(self, left_size: int, left_id: int, right_id: int) -> "Block":
        assert(left_size < self.size)
        new_block = Block(left_id, left_size, self.prev)
        self.id = right_id
        self.size -= left_size
        self.prev = new_block
        new_block.next = self
        return new_block
    
    def fill(self, other: "Block"):
        assert(self.is_free() and not other.is_free())
        if other.size == self.size:
            self.id = other.id
            other.id = -1
            other.merge_down()
        elif other.size < self.size:
            self.split(other.size, other.id, -1)
            other.id = -1
            other.merge_down()
        else:
            self.id = other.id
            other.split(other.size - self.size, other.id, -1)

    def merge_down(self):
        assert(self.is_free())
        while self.next is not None and self.next.id == -1:
            self.size += self.next.size
            self.next = self.next.next

    def checksum(self, pos: int) -> int:
        if self.is_free():
            return 0
        else:
            res = 0
            for i in range(self.size):
                res += (pos + i) * self.id
            return res
        
    def full_checksum(self) -> int:
        curr = self
        res = 0
        pos = 0
        while curr is not None:
            res += curr.checksum(pos)
            pos += curr.size
            curr = curr.next
        return res
        
    def __repr__(self):
        c = str(self.id) if self.id >= 0 else "."
        return c * self.size
    
    def full_chain_str(self):
        curr = self
        res = ""
        while curr is not None:
            res += str(curr)
            curr = curr.next
        return res
    
def generate_blocks(entry: List[str]):
    data = entry[0]
    blocks: List[Block] = []
    previous = None
    id = 0
    for i, c in enumerate(data):
        real_id = -1
        size = int(c)
        if (i & 1) == 0:
            real_id = id
            id += 1

        if size != 0:
            blocks.append(Block(real_id, size, previous))
            previous = blocks[-1]
    return blocks

@profile
def part_one(entry: List[str]) -> int:
    blocks = generate_blocks(entry)

    left_block = blocks[0]
    right_block = blocks[-1]
    while left_block != right_block:
        if not left_block.is_free():
            left_block = left_block.next
            continue
        if right_block.is_free():
            right_block = right_block.prev
            continue

        left_block.fill(right_block)

    return blocks[0].full_checksum()
    

@profile
def part_two(entry: List[str]) -> int:
    blocks = generate_blocks(entry)

    left_free = blocks[1]
    right_block = blocks[-1]

    i = 0
    while left_free != right_block:
        if not left_free.is_free():
            left_free = left_free.next
            continue

        if right_block.is_free():
            right_block = right_block.prev
            continue

        left_block = left_free
        moved = False
        while left_block != right_block:
            if left_block.is_free() and left_block.size >= right_block.size:
                left_block.fill(right_block)
                moved = True
                break
            left_block = left_block.next

        if not moved:
            right_block = right_block.prev

    return blocks[0].full_checksum()


if __name__ == "__main__":
    print("Part 1 example:", part_one(example_entries))
    print("Part 1 entry:", part_one(entries))

    print("Part 2 example:", part_two(example_entries))
    print("Part 2 entry:", part_two(entries))
