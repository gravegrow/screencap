from typing import Dict, List, Self

import cv2
import numpy
from rich.console import Console

from screencap.image import image

console = Console()


class Viewer:
    def __init__(self) -> None:
        self.images: Dict[str, numpy.ndarray] = {}
        self.blacklist: List[str] = []

        self._flags: int = cv2.WINDOW_AUTOSIZE | cv2.WINDOW_KEEPRATIO | cv2.WINDOW_GUI_NORMAL

    def ignore(self, name: str) -> Self:
        self.blacklist.append(name)
        return self

    def view(self, name: str, data: numpy.ndarray, height: int = 360) -> None:
        if name in self.blacklist:
            return

        if height > 0:
            data = image.set_height(data, height)

        cv2.namedWindow(name, flags=self._flags)
        cv2.imshow(name, data)

        if cv2.waitKey(1) == ord("q"):
            cv2.destroyWindow(name)
            self.ignore(name)

        return
