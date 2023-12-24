import math

class BitSet:
    def __init__(self, size: int):
        self.size = size
        self.field = [0] * math.ceil(self.size / 64)

    def set(self, bit: int):
        assert(bit < self.size)
        index = bit >> 6
        bit_n = bit & 0x3f
        self.field[index] |= (1 << bit_n)

    def reset(self, bit: int):
        assert(bit < self.size)
        index = bit >> 6
        bit_n = bit & 0x3f
        self.field[index] &= ~(1 << bit_n)

    def is_set(self, bit: int):
        assert(bit < self.size)
        index = bit >> 6
        bit_n = bit & 0x3f
        return (self.field[index] & (1 << bit_n)) != 0

    def __hash__(self) -> int:
        res = 0
        for word in self.field:
            res ^= word
        return res
    
    def __eq__(self, other: "BitSet") -> bool:
        return self.field == other.field