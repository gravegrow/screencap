from typing import List

import cv2

from screencap.capture import WindowCapture


class Previews:
    _pids: List[str]
    _captures: List[WindowCapture] = []

    is_running: bool = False

    def __init__(self, pids: List[str]):
        self._pids = pids

        for pid in self._pids:
            capture = WindowCapture(pid)
            # capture.set_max_height(250)
            capture.start()
            self._captures.append(capture)

    def stop(self) -> None:
        for capture in self._captures:
            cv2.destroyWindow(f"{capture}")

    def start(self):
        showing = 0
        while showing != len(self._pids):
            for capture in self._captures:
                capture.show()
                if capture.image.image is not None:
                    capture.stop()
                    showing += 1
