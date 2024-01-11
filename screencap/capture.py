import subprocess
from subprocess import CalledProcessError
from typing import Self

import cv2
import numpy as np
from mss import exception, mss

from screencap.geometry import Geometry
from screencap.image import Image
from screencap.pids import select_pid
from screencap.thread import Threaded
from screencap.window import Window


class WindowCapture(Threaded):
    process: str
    pid: str
    window: Window
    image: Image
    color_mode: int

    def set_size(self, width: int, height: int) -> Self:
        self._width = width
        self._height = height
        return self

    def show(self) -> None:
        if self.image.image is not None:
            self.image.show(f"WindowCapture - {self.process}")

    def __init__(self, process: str, color_mode: int = cv2.COLOR_BGR2GRAY):
        self.process = process
        self.pid = select_pid(self.process)
        self.window = Window(self.pid)
        self.color_mode = color_mode
        self.image = Image()

    def _execute(self) -> "WindowCapture":
        captured = self._capture_window()

        if captured is None:
            return self

        if self._width >= 0 and self._height >= 0:
            self.image.image = cv2.resize(captured, (self._width, self._height))
        else:
            self.image.image = captured

        return self

    def _capture_window(self) -> np.ndarray | None:
        if self.window.geometry is None:
            self.stop()
            raise SystemExit

        return self._capture_region(self.window.geometry)

    def _capture_region(self, geometry: Geometry) -> np.ndarray | None:
        with mss(with_cursor=True) as scr:
            try:
                image = scr.grab(geometry.region)
                return cv2.cvtColor(np.array(image), self.color_mode)
            except (exception.ScreenShotError, AttributeError) as _:
                return None

    _width: int = -1
    _height: int = -1
