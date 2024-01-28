from typing import Self

import numpy as np

from screencap.grabber import WindowGrabber
from screencap.image import Image
from screencap.processor import Processor
from screencap.viewer import Viewer


class WindowCapture(Processor):
    def __init__(self, pid: str, capture_height: int = 720):
        self.pid = pid
        self.grabber = WindowGrabber(pid)
        self.capture_height = capture_height

        self._preview: Viewer = Viewer()
        self._preview_height = 0

        self._img_key = "image"
        self._image: np.ndarray = self.grabber.grab()
        self.share(self._img_key, self._image)

    @property
    def image(self) -> np.ndarray:
        return self.get_shared(self._img_key)

    def show(self, height: int = 720) -> Self:
        self._preview_height = height
        return self

    def run(self):
        while self.running:
            self._image = Image.set_height(self.grabber.grab(), self.capture_height)
            self.share(self._img_key, self._image)

            if self._preview_height > 0:
                self._preview.view(self.pid, self._image, self._preview_height)
