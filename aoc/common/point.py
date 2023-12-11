import math

class Point:
    def __init__(self, x: int = 0, y: int = 0, z: int = 0):
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, other):
        if type(other) is float or type(other) is int:
            return Point(self.x + other, self.y + other, self.z + other)
        elif type(other) is Point:
            return Point(self.x + other.x, self.y + other.y, self.z + other.z)
        else:
            assert(False)

    def __mul__(self, other):
        if type(other) is float or type(other) is int:
            return Point(self.x * other, self.y * other, self.z * other)
        elif type(other) is Point:
            return Point(self.x * other.x, self.y * other.y, self.z * other.z)
        else:
            assert(False)

    def __sub__(self, other):
        if type(other) is float or type(other) is int:
            return Point(self.x - other, self.y - other, self.z - other)
        elif type(other) is Point:
            return Point(self.x - other.x, self.y - other.y, self.z - other.z)
        else:
            assert(False)
    
    def __eq__(self, other: "Point") -> bool:
        return self.x == other.x and self.y == other.y and self.z == other.z
    
    def __repr__(self) -> str:
        return f"({self.x}, {self.y}, {self.z})"
    
    def __hash__(self) -> int:
        return hash((self.x, self.y, self.z))
    
    def manathan_distance(self, other: "Point"):
        return abs(self.x - other.x) + abs(self.y - other.y) + abs(self.z - other.z)
    
    def squared_distance(self, other: "Point"):
        return (self.x - other.x) ** 2 + (self.y - other.y) ** 2 + (self.z - other.z) ** 2

    def distance(self, other: "Point"):
        return math.sqrt(self.squared_distance(other))
    
    def distance_inf(self, other: "Point"):
        return max(abs(self.x - other.x), abs(self.y - other.y), abs(self.z - other.z))
    
# return the intersection point, if it exists only a single one, and if it is on segment ab and if it is on segment cd
def intersect2D(a: Point, b: Point, c: Point, d: Point) -> bool:
    ab = b - a
    cd = d - c
    t = 0
    t_ = 0
    if ab.x != 0 and ab.y != 0 and cd.x != 0 and cd.y != 0:
        t_ = ((c.y - a.y) + ab.y * (c.x - a.x) / ab.x) / ((ab.y * cd.d) / ab.x - cd.y)
        t = (c.x - a.x + t_ * cd.x) / ab.x
    
    elif ab.x == 0:
        if cd.x == 0 or ab.y == 0:
            return None, 0, 0
        
        t_ = (a.x - c.x) / cd.x
        t = (c.y - a.y + t_ * cd.y) / ab.y
    
    elif ab.y == 0:
        if cd.y == 0:
            return None, 0, 0
        
        t_ = (a.y - c.y) / cd.y
        t = (c.x - a.x + t_ * cd.x) / ab.x
    
    else:    
        # Other cases are cd.x == 0 or cd.y == 0, so recall it in reverse
        inter, t_, t = intersect2D(c, d, a, b)
        return inter, t, t_

    return a + (ab * t), t, t_
