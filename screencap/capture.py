from dataclasses import dataclass, field

import cv2
import numpy as np
from mss import mss

from screencap.geometry import Geometry
from screencap.image import Image
from screencap.thread import Threaded
from screencap.window import Window


@dataclass
class WindowCapture(Threaded):
    process: str
    window: Window = field(init=False)
    image: Image = field(init=False, default_factory=Image)
    color_mode: int = cv2.COLOR_BGR2GRAY

    _width: int = -1
    _height: int = -1

    def set_size(self, width: int, height: int) -> "WindowCapture":
        self._width = width
        self._height = height
        return self

    def show(self) -> None:
        self.image.show(f"WindowCapture - {self.window.process}")

    def _execute(self) -> "WindowCapture":
        if self._width >= 0 and self._height >= 0:
            self.image.image = cv2.resize(self._capture_window(), (self._width, self._height))
        else:
            self.image.image = self._capture_window()

        return self

    def _capture_window(self) -> np.ndarray:
        if self.window.geometry:
            return self._capture_region(self.window.geometry)

        return np.zeros(())

    def _capture_region(self, geometry: Geometry) -> np.ndarray:
        with mss(with_cursor=True) as scr:
            image = scr.grab(geometry.region)
            return cv2.cvtColor(np.array(image), self.color_mode)

    def __post_init__(self):
        self.window = Window(self.process)
        self.window.choose()


if __name__ == "__main__":
    from rich import console

    capture = WindowCapture("gl")
    capture.set_size(1280, 720)
    capture.start()

    console.Console().print("Press 'Q' to exit.")

    while True:
        capture.show()

        if cv2.waitKey(1) == ord("q"):
            cv2.destroyAllWindows()
            capture.stop()
            break
