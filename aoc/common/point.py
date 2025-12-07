import itertools
import math
from typing import Optional, Tuple, Callable

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

    def __radd__(self, other):
        return self + other

    def __mul__(self, other):
        if type(other) is float or type(other) is int:
            return Point(self.x * other, self.y * other, self.z * other)
        elif type(other) is Point:
            return Point(self.x * other.x, self.y * other.y, self.z * other.z)
        else:
            assert(False)

    def __rmul__(self, other):
        return self * other

    def __truediv__(self, other):
        if type(other) is float or type(other) is int:
            return Point(self.x / other, self.y / other, self.z / other)
        elif type(other) is Point:
            return Point(self.x / other.x, self.y / other.y, self.z / other.z)
        else:
            assert(False)

    def __floordiv__(self, other):
        if type(other) is float or type(other) is int:
            return Point(self.x // other, self.y // other, self.z // other)
        elif type(other) is Point:
            return Point(self.x // other.x, self.y // other.y, self.z // other.z)
        else:
            assert(False)

    def __sub__(self, other):
        if type(other) is float or type(other) is int:
            return Point(self.x - other, self.y - other, self.z - other)
        elif type(other) is Point:
            return Point(self.x - other.x, self.y - other.y, self.z - other.z)
        else:
            assert(False)

    def __rsub__(self, other):
        return -self + other
    
    def __neg__(self):
        return self * -1
    
    def __eq__(self, other: "Point") -> bool:
        return self.x == other.x and self.y == other.y and self.z == other.z
    
    def __ne__(self, other: "Point") -> bool:
        return not (self == other)
    
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
    
    def __lt__(self, other: "Point"):
        return self.x < other.x and self.y < other.y and self.z < other.z
    
    def __gt__(self, other: "Point"):
        return self.x > other.x and self.y > other.y and self.z > other.z
    
    def dot(self, other: "Point") -> float:
        return self.x * other.x + self.y * other.y + self.z * other.z
    
    def __or__(self, other: "Point") -> float:
        return self.dot(other)
    
    def cross(self, other: "Point") -> "Point":
        return Point(self.y * other.z - self.z * other.y, self.z * other.x - self.x * other.z, self.x * other.y - self.y * other.x)
    
    def __xor__(self, other: "Point") -> "Point":
        return self.cross(other)
    
    def cross_2D(self, other: "Point") -> float:
        return self.x * other.y - self.y - other.x
    
    def squared_length(self) -> float:
        return self.dot(self)
    
    def length(self) -> float:
        return math.sqrt(self.squared_length())
    
    # Apply the result of the op between each x,y,z of self and other, in place
    def apply_op_in_place(self, other: "Point", op: Callable):
        self.x = op(self.x, other.x)
        self.y = op(self.y, other.y)
        self.z = op(self.z, other.z)
    
up = Point(-1, 0)
down = Point(1, 0)
left = Point(0, -1)
right = Point(0, 1)
    
# return the intersection point, if it exists only a single one, and if it is on segment ab and if it is on segment cd
def intersect_seg(a: Point, b: Point, c: Point, d: Point) -> Tuple[bool, Optional[Point], Optional[float], Optional[float]]:
    is_intersecting, impact, t, t_ = intersect(a, b - a, c, d - c)
    if not is_intersecting:
        return False, None, None, None
    return 0 <= t <= 1 and 0 <= t_ <= 1, impact, t, t_

# return the intersection point, if it exists only a single one
# Parameters are:
# a: Initial point of a line
# u: Direction of the line
# b: Initial point of the second line
# v: Direction of the second line
def intersect(a: Point, u: Point, b: Point, v: Point) -> Tuple[bool, Optional[Point], Optional[float], Optional[float]]:
    t = 0
    t_ = 0

    direction_cross = u.cross(v)

    # Parallel
    if direction_cross == Point():
        return False, None, None, None
    
    difference = b - a
    second_cross = difference.cross(v)

    # No intersection
    if direction_cross.cross(second_cross) != Point():
        return False, None, None, None
    
    t = second_cross.length() / direction_cross.length()
    if second_cross.dot(direction_cross) < 0:
        t = -t

    first_cross = difference.cross(u)
    t_ = first_cross.length() / direction_cross.length()
    if first_cross.dot(direction_cross) < 0:
        t_ = -t_
    
    impact = u * t + a
    return True, impact, t, t_
