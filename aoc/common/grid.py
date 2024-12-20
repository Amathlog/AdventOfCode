from aoc.common.point import Point
from typing import List, Any, Iterable

class Grid:
    def __init__(self, grid: List[List[Any]]) -> None:
        self.grid = grid
        self.max_x = len(self.grid)
        self.max_y = len(self.grid[0] if len(self.grid) > 0 else 0)

    @staticmethod
    def as_int_grid(grid: Iterable[Iterable[Any]]) -> "Grid":
        return Grid([[int(a) for a in line] for line in grid])

    def is_valid_xy(self, x: int, y: int) -> bool:
        return x >= 0 and y >= 0 and x < self.max_x and y < self.max_y

    def is_valid(self, p: Point) -> bool:
        return self.is_valid_xy(p.x, p.y)
    
    def get(self, x: int, y: int) -> Any:
        return self.grid[x][y]
    
    def set(self, x: int, y: int, v: Any) -> None:
        self.grid[x][y] = v
    
    def __getitem__(self, p: Point) -> Any:
        return self.get(p.x, p.y)
    
    def __setitem__(self, p: Point, v: Any) -> None:
        self.set(p.x, p.y, v)
    
    def __repr__(self) -> str:
        return str(self.grid)
    
    def pretty_str(self, cell_size = 1, separator = "") -> str:
        res = ""
        for line in self.grid:
            if type(line) is str:
                res += line + '\n'
            else:
                line_str = [str(v) for v in line]
                if cell_size > 1:
                    for i in range(len(line_str)):
                        if len(line_str[i]) < cell_size:
                            line_str[i] += " " * (cell_size - len(line_str[i]))

                res += separator.join(line_str) + '\n'
        return res
    
    def __eq__(self, other: "Grid") -> bool:
        return self.grid == other.grid
    
    def __hash__(self) -> int:
        return hash(tuple([tuple(x) for x in self.grid]))
