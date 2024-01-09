from dataclasses import dataclass, field

import cv2
import numpy as np
from mss import mss

from screencap.geometry import Geometry
from screencap.image import Image
from screencap.window import Window


@dataclass
class WindowCapture:
    process: str
    window: Window = field(init=False)
    image: Image = field(init=False, default_factory=Image)

    _width: int = -1
    _height: int = -1

    def __post_init__(self):
        self.window = Window(self.process)
        self.window.choose()

    def set_size(self, width: int, height: int) -> "WindowCapture":
        self._width = width
        self._height = height
        return self

    def show(self) -> None:
        self.image.show(f"WindowCapture - {self.window.process}")

    def run(self, color: int = cv2.COLOR_RGB2GRAY) -> "WindowCapture":
        if self._width >= 0 and self._height >= 0:
            self.image.image = cv2.resize(self._capture_window(), (self._width, self._height))
        else:
            self.image.image = self._capture_window()

        self.image.image = cv2.cvtColor(self.image.image, color)

        return self

    def _capture_window(self) -> np.ndarray:
        if self.window.geometry:
            return self._capture_region(self.window.geometry)

        return np.zeros(())

    def _capture_region(self, geometry: Geometry) -> np.ndarray:
        with mss(with_cursor=True) as scr:
            image = scr.grab(geometry.region)
            return np.array(image)


if __name__ == "__main__":
    from rich import console

    capture = WindowCapture("gl")
    capture.set_size(1280, 720)

    console.Console().print("Press 'Q' to exit.")

    while True:
        capture.run().show()

        if cv2.waitKey(1) == ord("q"):
            cv2.destroyAllWindows()
            break
