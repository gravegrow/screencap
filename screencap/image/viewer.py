from typing import Dict, List, Self

import cv2
import numpy
from rich.console import Console

from screencap.image.image import Image

console = Console()


class Viewer:
    def __init__(self, height: int = -1) -> None:
        self.images: Dict[str, Image] = {}
        self.height = height
        self.blacklist: List[str] = []
        self._flags: int = cv2.WINDOW_AUTOSIZE | cv2.WINDOW_KEEPRATIO | cv2.WINDOW_GUI_NORMAL

    def ignore(self, name: str) -> Self:
        self.blacklist.append(name)
        return self

    def view(self, name: str, data: numpy.ndarray | None) -> Self:
        if name in self.blacklist or data is None:
            return self

        if self.height > 0:
            width = int(data.shape[1] * (self.height / data.shape[0]))
            data = cv2.resize(data, (width, self.height))

        cv2.namedWindow(name, flags=self._flags)
        cv2.imshow(name, data)

        if cv2.waitKey(1) == ord("q"):
            cv2.destroyWindow(name)
            self.ignore(name)
            console.log(f"View '{name}' has been closed.")

        return self
