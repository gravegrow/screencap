from typing import Self

import numpy

from screencap.grabber import WindowGrabber
from screencap.image import image
from screencap.processor import Processor
from screencap.viewer import Viewer


class WindowCapture(Processor):
    def __init__(self, pid: str, cap_height: int = 720):
        self.pid = pid
        self.grabber = WindowGrabber(pid)
        self.capture_height = cap_height
        self.image: numpy.ndarray = image.set_height(self.grabber.grab(), cap_height)

        self._viewer: Viewer = Viewer()
        self._viewer_name = f"{self.pid}"
        self._viewer_height = 0

    def show(self, height: int = 720) -> Self:
        with self.lock:
            self._viewer_height = height
            return self

    def run(self):
        while self.is_running:
            # with self.lock:
            self.image = image.set_height(self.grabber.grab(), self.capture_height)

            if self._viewer_height > 0:
                self._viewer.view(self._viewer_name, self.image, self._viewer_height)
