from dataclasses import dataclass
from typing import Tuple

import cv2
import numpy as np

from screencap.image.area import Area


def crop(source: np.ndarray, area: Area) -> np.ndarray:
    return source[
        area.y : min(area.y_bounds, source.shape[0]),
        area.x : min(area.x_bounds, source.shape[1]),
    ]


def search(
    source: np.ndarray, target: np.ndarray, min_thresh: float = 0.7
) -> Tuple[int, int] | None:
    threshold = 1.0
    result = None

    while threshold >= min_thresh:
        match = cv2.matchTemplate(source, cv2.Mat(target), cv2.TM_CCOEFF_NORMED)
        locations = np.where(match >= threshold)

        if len(locations[0]) > 0:
            result = (int(np.mean(locations[1])), int(np.mean(locations[0])))
            break

        threshold -= 0.01

    return result


def set_height(source: np.ndarray, height: int) -> np.ndarray:
    width = source.shape[1] * (height / source.shape[0])
    return cv2.resize(source, (int(width), height))


@dataclass
class IdDrawer:
    scale: float = 7
    offset: int = 70
    thickness: int = 6

    def draw(self, index: int, data: np.ndarray) -> np.ndarray:
        origin = (int(data.shape[1] / 2) - self.offset, int(data.shape[0] / 2) + self.offset)

        for color, thickness in ((0, self.thickness * 2), (255, self.thickness)):
            data = cv2.putText(
                data,
                str(index),
                origin,
                cv2.FONT_HERSHEY_DUPLEX,
                self.scale,
                color,
                thickness,
            )

        return data
