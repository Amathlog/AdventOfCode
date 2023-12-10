from aoc.common.point import Point
from typing import List, Any

class Grid:
    def __init__(self, grid: List[List[Any]]) -> None:
        self.grid = grid
        self.max_x = len(self.grid)
        self.max_y = len(self.grid[0] if len(self.grid) > 0 else 0)

    def is_valid_xy(self, x: int, y: int):
        return x >= 0 and y >= 0 and x < self.max_x and y < self.max_y

    def is_valid(self, p: Point):
        return self.is_valid_xy(p.x, p.y)
    
    def get(self, x: int, y: int):
        return self.grid[x][y]
    
    def __getitem__(self, p: Point):
        return self.get(p.x, p.y)
    
    def __repr__(self) -> str:
        return str(self.grid)
