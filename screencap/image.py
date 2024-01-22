from typing import Self, Tuple, Union

import cv2
import numpy as np

from screencap.geometry import Geometry


class Image:
    image: np.ndarray | None

    def __init__(self, image: np.ndarray | None = None) -> None:
        self.image = image

    def find(self, image: "Image", threshold: float = 0.8) -> None | Tuple[int, int]:
        if self.image is None or image.image is None:
            return None

        needle = cv2.Mat(image.image)
        result = cv2.matchTemplate(self.image, needle, cv2.TM_CCOEFF_NORMED)

        location = np.where(result >= threshold)

        if len(location[0]) <= 0:
            return None

        return int(np.mean(location[1])), int(np.mean(location[0]))

    def show(self, name: str) -> None:
        if self.image is None or self.image.shape[0] <= 1:
            return

        flags = cv2.WINDOW_AUTOSIZE | cv2.WINDOW_KEEPRATIO | cv2.WINDOW_GUI_NORMAL
        cv2.namedWindow(name, flags=flags)
        cv2.imshow(name, self.image)

    def crop(self, region: Union[Geometry, Tuple[int, int, int, int]]) -> "Image":
        if self.image is None:
            return self

        if isinstance(region, Tuple):
            self._crop_geo.x, self._crop_geo.y, self._crop_geo.width, self._crop_geo.height = region
            region = self._crop_geo

        cropped = self.image[
            region.y : min(region.y_bounds, self.image[0].size),
            region.x : min(region.x_bounds, self.image[1].size),
        ]

        return Image(cropped)

    _crop_geo: Geometry = Geometry(0, 0, 0, 0)
