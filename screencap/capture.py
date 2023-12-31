from dataclasses import dataclass, field

import cv2
import numpy as np
from mss import mss

from screencap.thread import Threaded
from screencap.window import Geometry, Window


@dataclass
class Screen:
    screen: np.ndarray

    def show(self, name: str = "Screen"):
        if self.screen.size > 1:
            flags = cv2.WINDOW_AUTOSIZE | cv2.WINDOW_KEEPRATIO | cv2.WINDOW_GUI_NORMAL
            cv2.namedWindow(name, flags=flags)
            cv2.imshow(name, self.screen)


@dataclass
class WindowCapture(Threaded, Screen):
    window: Window
    screen: np.ndarray = field(init=False, default_factory=lambda: np.zeros(()))

    def crop(self, region: Geometry) -> Screen:
        if self.screen.size > 1:
            crop = self.screen[region.y : region.y_bounds, region.x : region.x_bounds]
            return Screen(crop)

        return Screen(np.zeros(()))

    def _execute(self) -> None:
        self.screen = self._capture_window()

    def _capture_window(self) -> np.ndarray:
        return self._capture_region(self.window.geometry)

    def _capture_region(self, geometry: Geometry) -> np.ndarray:
        with mss(with_cursor=True) as scr:
            image = scr.grab(geometry.region)
            return np.array(image)


if __name__ == "__main__":
    window = Window("Navigator")
    capture = WindowCapture(window)
    capture.start()

    while True:
        capture.show()
        capture.crop(Geometry(5, 5, 20, 20)).show("new")

        if cv2.waitKey(1) == ord("q"):
            cv2.destroyAllWindows()
            capture.stop()
            break
