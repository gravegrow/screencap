from dataclasses import dataclass
from typing import Self, Tuple

import screeninfo


@dataclass
class Geometry:
    x: int = 0
    y: int = 0
    width: int = 1
    height: int = 1

    def set_dimensions(self, x: int, y: int, width: int, height: int) -> Self:
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        return self

    @property
    def x_bounds(self):
        return self.x + self.width

    @property
    def y_bounds(self):
        return self.y + self.height

    @property
    def region(self) -> Tuple[int, int, int, int]:
        return max(self.x, 0), max(self.y, 0), self.x_bounds, self.y_bounds


@dataclass
class WindowGeometry(Geometry):
    desktop_width: int = 0
    desktop_height: int = 0

    def __post_init__(self):
        for monitor in screeninfo.get_monitors():
            self.desktop_width += monitor.width

        self.desktop_height = min((monitor.height for monitor in screeninfo.get_monitors()))

    @property
    def x_bounds(self):
        return min(self.x + self.width, self.desktop_width)

    @property
    def y_bounds(self):
        return min(self.y + self.height, self.desktop_height)
