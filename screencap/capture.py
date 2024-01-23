from typing import Self

import cv2
import numpy as np
from mss import exception, mss

from screencap.geometry import Geometry
from screencap.image import Image
from screencap.image_view import ImageProvider
from screencap.thread import Threaded
from screencap.window import Window


class WindowCapture(ImageProvider):
    pid: str
    window: Window
    color_mode: int

    def set_max_height(self, height: int = 100) -> Self:
        self._max_height = height
        return self

    def set_size(self, width: int, height: int) -> Self:
        self._width = width
        self._height = height
        return self

    def show(self, name: str = "WindowCapture") -> None:
        if self.image.image is not None:
            self.image.show(f"{name} | PID: {self.pid}")

    def run(self) -> "WindowCapture":
        captured = self._capture_window()

        if captured is None:
            return self

        if self._width > 0 and self._height > 0:
            self.image.image = cv2.resize(captured, (self._width, self._height))

        elif self._max_height > 0:
            scale = self._max_height / captured.shape[0]
            self.image.image = cv2.resize(
                captured, (int(captured.shape[1] * scale), self._max_height)
            )
        else:
            self.image.image = captured

        return self

    def _capture_window(self) -> np.ndarray | None:
        if self.window.geometry is None:
            raise SystemExit

        return self._capture_region(self.window.geometry)

    def _capture_region(self, geometry: Geometry) -> np.ndarray | None:
        with mss(with_cursor=True) as scr:
            try:
                image = scr.grab(geometry.region)
                return cv2.cvtColor(np.array(image), self.color_mode)
            except (exception.ScreenShotError, AttributeError) as _:
                return None

    def __init__(self, pid: str, color_mode: int = cv2.COLOR_BGR2GRAY):
        self.pid = pid
        self.window = Window(self.pid)
        self.color_mode = color_mode

    _width: int = -1
    _height: int = -1
    _max_height: int = -1
