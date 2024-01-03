import tkinter
from dataclasses import dataclass, field
from typing import Tuple


@dataclass
class Geometry:
    x: int
    y: int
    width: int
    height: int

    @property
    def x_bounds(self):
        return min(self.x + self.width, self._root.winfo_screenwidth())

    @property
    def y_bounds(self):
        return min(self.y + self.height, self._root.winfo_screenheight())

    @property
    def region(self) -> Tuple[int, int, int, int]:
        return max(self.x, 0), max(self.y, 0), self.x_bounds, self.y_bounds

    _root: tkinter.Tk = field(init=False, default_factory=tkinter.Tk)
