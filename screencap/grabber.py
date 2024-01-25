from typing import Self

import cv2
import numpy
from Xlib import X, display, error, ext


class WindowGrabber:
    trim: int = 0
    last: numpy.ndarray

    def __init__(self, pid: str):
        super().__init__()

        self.pid = pid
        self._window = display.Display().create_resource_object("window", int(pid))
        ext.composite.redirect_window(self._window, 0)  # type: ignore

        geo = self._window.get_geometry()
        self.last = numpy.zeros((geo.width, geo.height))

    def set_trim(self, value: int) -> Self:
        self.trim = value
        return self

    def grab(self) -> numpy.ndarray:
        try:
            geo = self._window.get_geometry()
            width, height = geo.width - self.trim, geo.height - self.trim
            pixmap = self._window.get_image(0, 0, width, height, X.ZPixmap, 0xFFFFFFFF)

        except error.BadMatch as _:
            return self.last

        self.last = numpy.frombuffer(pixmap.data, dtype="uint8").reshape((height, width, 4))
        self.last = cv2.cvtColor(self.last, cv2.COLOR_RGB2GRAY)

        return self.last
