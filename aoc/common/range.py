from typing import Optional, List

class Range:
    def __init__(self, min: int, max: int):
        assert(min <= max)
        self.min = min
        self.max = max

    def overlaps(self, other: "Range", inclusive: bool) -> bool:
        if self > other:
            return other.overlaps(self, inclusive)
        
        if inclusive:
            return other.min <= self.max
        else:
            return other.min < self.max
        
    def merge(self, other: "Range", inclusive: bool) -> Optional["Range"]:
        if not self.overlaps(other, inclusive):
            return None
        
        if self > other:
            return other.merge(self, inclusive)
        
        return Range(self.min, max(self.max, other.max))
        
    def contains(self, v: int, inclusive: bool) -> bool:
        if inclusive:
            return self.min <= v <= self.max
        else:
            return self.min < v < self.max
        
    def __lt__(self, other: "Range") -> bool:
        return self.min < other.min
    
    def __gt__(self, other: "Range") -> bool:
        return self.min > other.min

    def __hash__(self):
        return hash((self.x, self.y))
        
    def __repr__(self):
        return f"{self.min}-{self.max}"
    
    @staticmethod
    def reduce(ranges: List["Range"], inclusive: bool) -> List["Range"]:
        ranges = sorted(ranges)
        result = [ranges[0]]
        for r in ranges[1:]:
            merge = result[-1].merge(r, inclusive)
            if merge is not None:
                result[-1] = merge
            else:
                result.append(r)

        return result
