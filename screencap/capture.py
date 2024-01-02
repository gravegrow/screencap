from dataclasses import dataclass, field

import cv2
import numpy as np
from mss import mss

from screencap.image import Image
from screencap.thread import Threaded
from screencap.window import Geometry, Window


@dataclass
class WindowCapture(Threaded):
    window: Window
    image: Image = field(init=False, default_factory=Image)

    def show(self) -> None:
        self.image.show("Capture")

    def _execute(self) -> None:
        self.image.image = self._capture_window()

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

    print("Press 'Q' to exit.")

    while True:
        capture.show()
        tab = capture.image.crop((230, 0, 220, 48))
        tab.show("tab")

        if cv2.waitKey(1) == ord("q"):
            cv2.destroyAllWindows()
            capture.stop()
            break
