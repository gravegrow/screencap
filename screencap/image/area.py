from dataclasses import dataclass
from typing import Self, Tuple


@dataclass
class Area:
    x: int = 0
    y: int = 0
    width: int = 1
    height: int = 1

    @property
    def x_bounds(self):
        return self.x + self.width

    @property
    def y_bounds(self):
        return self.y + self.height

    @property
    def region(self) -> Tuple[int, int, int, int]:
        return max(self.x, 0), max(self.y, 0), self.x_bounds, self.y_bounds

    def set_dimensions(self, x: int, y: int, width: int, height: int) -> Self:
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        return self
