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
