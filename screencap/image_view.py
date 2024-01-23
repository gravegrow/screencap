from abc import ABC
from typing import Dict, Self

import cv2

from screencap.image import Image
from screencap.thread import Threaded


class ImageProvider(ABC):
    image: Image = Image()


class ImageView(Threaded, ImageProvider):
    images: Dict[str, ImageProvider]

    _flags: int = cv2.WINDOW_AUTOSIZE | cv2.WINDOW_KEEPRATIO | cv2.WINDOW_GUI_NORMAL

    def __init__(self) -> None:
        self.images = {}

    def start(self) -> Self:
        super().start()
        return self

    def watch(self, name: str, source: ImageProvider):
        self.images[name] = source

    def _execute(self):
        for name, source in self.images.items():
            if source.image.image is None:
                continue

            cv2.namedWindow(name, flags=self._flags)
            cv2.imshow(name, source.image.image)
