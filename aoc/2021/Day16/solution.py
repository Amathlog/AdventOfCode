from pathlib import Path
import os
import copy
from functools import reduce

entry_file = Path(os.path.abspath(__file__)).parent / "entry.txt"
example_file = Path(os.path.abspath(__file__)).parent / "example.txt"

with entry_file.open("r") as f:
    entries = f.readlines()

for i in range(len(entries)):
    if entries[i][-1] == '\n':
        entries[i] = entries[i][:-1]

class DecodeVisitor:
    def __init__(self, msg: str):
        self.msg = msg
        self.current_decode = ""

    def remaining(self):
        return len(self.msg) * 4 + len(self.current_decode)

    def read(self, nb_bits: int):
        if nb_bits > len(self.current_decode):
            nb_expand = (nb_bits - len(self.current_decode) - 1) // 4 + 1
            self.expand(nb_expand)
        res = self.current_decode[:nb_bits]
        self.current_decode = self.current_decode[nb_bits:]
        return res

    def expand(self, nb_expand: int = 1):
        c = int(self.msg[:nb_expand], base=16)
        c = str(bin(c))[2:].rjust(4 * nb_expand, '0') # remove '0b' and add 0 at the left
        self.current_decode = self.current_decode + c
        self.msg = self.msg[nb_expand:]

class Packet:
    def __init__(self, visitor):
        self.version = int(visitor.read(3), base=2)
        self.id = int(visitor.read(3), base=2)

        if self.id == 4:
            self.content = Litteral(visitor)
            self.is_litteral = True
        else:
            self.content = Operator(self.id, visitor)
            self.is_litteral = False

    def __repr__(self) -> str:
        if self.is_litteral:
            return f"v: {self.version}: litteral: {str(self.content)}"
        else:
            return f"v: {self.version}; id: {self.id}; operator: ({self.content})"

    def version_sum(self):
        return self.version + self.content.version_sum()

    def operate(self):
        return self.content.operate()


class Litteral:
    def __init__(self, visitor):
        self.number = ""
        while True:
            temp = visitor.read(5)
            self.number += temp[1:]
            if temp[0] == '0':
                break
        self.number = int(self.number, base=2)

    def __repr__(self) -> str:
        return str(self.number)
    
    def version_sum(self):
        return 0

    def operate(self):
        return self.number

class Operator:
    def __init__(self, id, visitor):
        self.id = id
        self.type_id = visitor.read(1)
        self.contents = []
        if self.type_id == '0':
            # 15-bit mode
            length = int(visitor.read(15), base=2)
            end_remaining = visitor.remaining() - length
            while visitor.remaining() > end_remaining:
                self.contents.append(Packet(visitor))
        else:
            nb_reads = int(visitor.read(11), base=2)
            self.contents = [Packet(visitor) for _ in range(nb_reads)]

    def __repr__(self) -> str:
        return str(self.contents)

    def version_sum(self):
        res = 0
        for c in self.contents:
            res += c.version_sum()

        return res

    def operate(self):
        res = [c.operate() for c in self.contents]
        if (self.id == 0):
            return sum(res)
        elif (self.id == 1):
            return reduce(lambda a,b: a * b, res)
        elif (self.id == 2):
            return min(res)
        elif (self.id == 3):
            return max(res)
        elif (self.id == 5):
            return int(res[0] > res[1])
        elif (self.id == 6):
            return int(res[0] < res[1])
        elif (self.id == 7):
            return int(res[0] == res[1])

if __name__ == "__main__":
    visitor = DecodeVisitor(entries[0])
    packet = Packet(visitor)
    print("First answer:", packet.version_sum())
    print("Second answer:", packet.operate())