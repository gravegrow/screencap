from typing import Tuple, Union

import cv2
import numpy as np

from screencap.area import Area


class Image:
    data: np.ndarray | None

    def __init__(self, data: np.ndarray | None = None) -> None:
        self.data = data

    @property
    def shape(self):
        return self.data.shape if self.data is not None else (0, 0)

    def search(self, data: np.ndarray, threshold: float = 0.8) -> None | Tuple[int, int]:
        if self.data is None or data is None:
            return None

        needle = cv2.Mat(data)
        result = cv2.matchTemplate(self.data, needle, cv2.TM_CCOEFF_NORMED)
        location = np.where(result >= threshold)

        if len(location[0]) <= 0:
            return None

        return int(np.mean(location[1])), int(np.mean(location[0]))

    def crop(self, region: Union[Area, Tuple[int, int, int, int]]) -> "Image":
        if self.data is None:
            return self

        if isinstance(region, Tuple):
            (
                self._crop_area.x,
                self._crop_area.y,
                self._crop_area.width,
                self._crop_area.height,
            ) = region
            region = self._crop_area

        cropped = self.data[
            region.y : min(region.y_bounds, self.data[0].size),
            region.x : min(region.x_bounds, self.data[1].size),
        ]

        return Image(cropped)

    _crop_area: Area = Area()
