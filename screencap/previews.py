from dataclasses import dataclass
from multiprocessing import Process
from typing import List

import cv2
import numpy

from screencap.grabber import WindowGrabber
from screencap.image.viewer import Viewer


@dataclass
class IdDrawer:
    scale: float = 7
    offset: int = 70
    thickness: int = 6

    def draw(self, index: int, data: numpy.ndarray) -> numpy.ndarray:
        origin = (int(data.shape[1] / 2) - 70, int(data.shape[0] / 2) + 70)

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


class Previews(Process):
    def __init__(self, pids: List[str], height: int = 360):
        super().__init__()
        self.pids = pids
        self.id_drawer = IdDrawer()
        self.viewer = Viewer(height)
        self.height = height
        self.grabbers: List[WindowGrabber] = []
        self.name = "Previews"
        self.is_running = True

        for pid in pids:
            grabber = WindowGrabber(pid)
            self.grabbers.append(grabber)

    def generate_preview(self) -> numpy.ndarray:
        previews = []
        for index, grabber in enumerate(self.grabbers):
            data = grabber.grab()
            width = data.shape[1] * (self.height / data.shape[0])
            data = cv2.resize(data, (int(width), self.height))
            data = self.id_drawer.draw(index + 1, data)
            previews.append(data)

        return numpy.concatenate(previews, axis=1)

    def run(self) -> None:
        while self.is_running:
            self.viewer.view(self.name, self.generate_preview())

    def stop(self) -> None:
        cv2.destroyWindow(self.name)
        self.is_running = False
