from dataclasses import dataclass
from typing import List

import cv2
import numpy

from screencap import image
from screencap.grabber import WindowGrabber
from screencap.pids.manager import PidManager
from screencap.processor import Processor
from screencap.viewer import Viewer


def SelectPidPreviews(process: str, height=360) -> str:
    pids = PidManager(process)
    previews = Previews(pids.pids, height).start()
    pid = pids.select()
    previews.stop()
    return pid


class Previews(Processor):
    def __init__(self, pids: List[str], height: int = 360):
        self.pids = pids
        self.id_drawer = IdDrawer(scale=height / 50, offset=int(height / 5))
        self.viewer: Viewer = Viewer()
        self.height = height
        self.grabbers: List[WindowGrabber] = []

        for pid in pids:
            grabber = WindowGrabber(pid)
            self.grabbers.append(grabber)

    def run(self) -> None:
        while self.is_running:
            self.viewer.view("Previews", self.generate_preview())

    def generate_preview(self) -> numpy.ndarray:
        previews = []
        for index, grabber in enumerate(self.grabbers):
            data = grabber.grab()
            data = image.set_height(data, self.height)
            data = self.id_drawer.draw(index + 1, data)
            previews.append(data)

        return numpy.concatenate(previews, axis=1)


@dataclass
class IdDrawer:
    scale: float = 7
    offset: int = 70
    thickness: int = 6

    def draw(self, index: int, data: numpy.ndarray) -> numpy.ndarray:
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
