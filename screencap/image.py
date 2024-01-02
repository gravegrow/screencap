from abc import ABC
from dataclasses import dataclass, field
from typing import Tuple, Union

import cv2
import numpy as np

from screencap.window import Geometry


@dataclass
class Image(ABC):
    image: np.ndarray = field(default_factory=lambda: np.zeros(()))
    _crop: Geometry = field(init=False, default_factory=lambda: Geometry(0, 0, 0, 0))

    def show(self, name: str) -> None:
        if self.image.size <= 1:
            return

        flags = cv2.WINDOW_AUTOSIZE | cv2.WINDOW_KEEPRATIO | cv2.WINDOW_GUI_NORMAL
        cv2.namedWindow(name, flags=flags)
        cv2.imshow(name, self.image)

    def crop(self, region: Union[Geometry, Tuple[int, int, int, int]]) -> "Image":
        if self.image.size <= 1:
            return self

        if isinstance(region, Tuple):
            self._crop.x, self._crop.y, self._crop.width, self._crop.height = region
            region = self._crop

        return Image(
            self.image[
                region.y : min(region.y_bounds, self.image[0].size),
                region.x : min(region.x_bounds, self.image[1].size),
            ]
        )
