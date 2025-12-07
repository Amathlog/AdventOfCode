import itertools
import math
from typing import Optional, Tuple, Callable, Generator, Union, List

Numeric = Union[int, float]
NumericOrVector = Union[Numeric, "Vector"]

# Generic class that represents Vector2, Vector3 and Vector4
# Can access components with x, y, z and w. If an invalid component is accessed (like z on a Vec2) it returns 0
class Vector:
    def __init__(self, *args: Numeric) -> None:
        assert(len(args) >= 2 and len(args) <= 4)
        self.values: List[Numeric] = list(args)

    def __len__(self) -> int:
        return len(self.values)
    
    def __getitem__(self, idx: int) -> Numeric:
        return self.values[idx] if idx < len(self.values) else 0
    
    def set_value(self, idx: int, v: Numeric) -> None:
        if idx < len(self.values):
            self.values[idx] = v

    @property
    def x(self) -> Numeric:
        return self[0]
    
    @x.setter
    def x(self, v: Numeric) -> None:
        self.set_value(0, v)
    
    @property
    def y(self) -> Numeric:
        return self[1]
    
    @y.setter
    def y(self, v: Numeric) -> None:
        self.set_value(1, v)
    
    @property
    def z(self) -> Numeric:
        return self[2]
    
    @z.setter
    def z(self, v: Numeric) -> None:
        self.set_value(2, v)
    
    @property
    def w(self) -> Numeric:
        return self[3]
    
    @w.setter
    def w(self, v: Numeric) -> None:
        self.set_value(3, v)
    
    ## Utilities
    # Create a generator that return a tuple of zipped values between self and other.
    # Use the dimension of self.
    def zip(self, other: "Vector") -> Generator[Numeric, Numeric]:
        for i in range(len(self)):
            yield self[i], other[i]
    
    def apply_in_place(self, op: Callable[[Numeric], Numeric]) -> None:
        self.values = list(map(op, self.values))

    def apply(self, op: Callable[[Numeric], Numeric]) -> "Vector":
        return self.__class__(*map(op, self.values))

    def apply_in_place_with_other(self, other: "Vector", op: Callable[[Numeric, Numeric], Numeric]) -> None:
        self.values = list(itertools.starmap(op, self.zip(other)))

    def apply_with_other(self, other: "Vector", op: Callable[[Numeric, Numeric], Numeric]) -> "Vector":
       return self.__class__(*itertools.starmap(op, self.zip(other)))
    
    ## Maths oprations and overloads
    def math_op(self, other: NumericOrVector, op: Callable[[Numeric, Numeric], Numeric]) -> "Vector":
        if isinstance(other, float) or isinstance(other, int):
            return self.apply(lambda a: op(a, other))
        elif isinstance(other, Vector):
            return self.apply_with_other(other, op)
        else:
            assert(False)
    
    def __add__(self, other: NumericOrVector) -> "Vector":
        return self.math_op(other, lambda a,b: a+b)

    def __mul__(self, other: NumericOrVector) -> "Vector":
        return self.math_op(other, lambda a,b: a*b)
    
    def __sub__(self, other: NumericOrVector) -> "Vector":
        return self.math_op(other, lambda a,b: a-b)
    
    def __truediv__(self, other: NumericOrVector) -> "Vector":
        return self.math_op(other, lambda a,b: a/b)
    
    def __floordiv__(self, other: NumericOrVector) -> "Vector":
        return self.math_op(other, lambda a,b: a//b)
    
    def __neg__(self) -> "Vector":
        return self * -1
    
    # String overload
    def __repr__(self) -> str:
        return str(tuple(self.values))
    
    # Hash overload
    def __hash__(self) -> int:
        return hash(self.values)
    
    ## Distances
    def manathan_distance(self, other: "Vector") -> Numeric:
        return sum((abs(a - b) for a,b in self.zip(other)))
    
    def squared_distance(self, other: "Vector") -> Numeric:
        return sum(((a - b)**2 for a,b in self.zip(other)))

    def distance(self, other: "Vector") -> float:
        return math.sqrt(self.squared_distance(other))
    
    def distance_inf(self, other: "Vector") -> Numeric:
        return max((a - b for a,b in self.zip(other)))
    
    ## Comparison overloads
    def __eq__(self, other: "Vector") -> bool:
        return all((a == b for a,b in self.zip(other)))
    
    def __ne__(self, other: "Vector") -> bool:
        return not (self == other)
    
    def __lt__(self, other: "Vector") -> bool:
        return all((a < b for a,b in self.zip(other)))
    
    def __le__(self, other: "Vector") -> bool:
        return all((a <= b for a,b in self.zip(other)))
    
    def __gt__(self, other: "Vector") -> bool:
        return all((a > b for a,b in self.zip(other)))
    
    def __ge__(self, other: "Vector") -> bool:
        return all((a >= b for a,b in self.zip(other)))
    
    ## Algebra operations
    # Dot is defined for all vectors. Can also use a | b.
    def dot(self, other: "Vector") -> Numeric:
        return sum((a * b for a,b in self.zip(other)))
    
    def __or__(self, other: "Vector") -> Numeric:
        return self.dot(other)
    
    # Cross is defined for Vec2 (returns a Numeric) or Vec3 (returns a Vec3). Vec4 returns None.
    def cross(self, other: "Vector") -> Union[Numeric, "Vector", None]:
        if len(self) == 2:
            return self.x * other.y - self.y - other.x
        elif len(self) == 3:
            return self.__class__(self.y * other.z - self.z * other.y, self.z * other.x - self.x * other.z, self.x * other.y - self.y * other.x)
        else:
            return None
    
    def __xor__(self, other: "Vector") -> "Vector":
        return self.cross(other)
    
    def cross_2D(self, other: "Vector") -> Numeric:
        return self.x * other.y - self.y - other.x
    
    def squared_length(self) -> Numeric:
        return self.dot(self)
    
    def length(self) -> float:
        return math.sqrt(self.squared_length())


class Vector2(Vector):
    def __init__(self, x: int = 0, y: int = 0):
        super().__init__(x, y)

    @staticmethod
    def cast(other: "Vector") -> "Vector2":
        return Vector2(other.x, other.y)


class Vector3(Vector):
    def __init__(self, x: int = 0, y: int = 0, z: int = 0):
        super().__init__(x, y, z)

    @staticmethod
    def cast(other: "Vector") -> "Vector3":
        return Vector3(other.x, other.y, other.z)


class Vector4(Vector):
    def __init__(self, x: int = 0, y: int = 0, z: int = 0, w: int = 0):
        super().__init__(x, y, z, w)

    @staticmethod
    def cast(other: "Vector") -> "Vector4":
        return Vector4(other.x, other.y, other.z, other.w)
