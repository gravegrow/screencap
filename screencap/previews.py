from typing import List

import numpy

from screencap.grabber import WindowGrabber
from screencap.image import Image
from screencap.pids.manager import PidManager
from screencap.processor import Processor
from screencap.viewer import Viewer


def PIDSelect(process: str, height=360) -> str:
    pids = PidManager(process)
    previews = Previews(pids.pids, height).start()
    pid = pids.select()
    previews.stop()
    return pid


class Previews(Processor):
    def __init__(self, pids: List[str], height: int = 360):
        self.pids = pids
        self.id_drawer = Image.IdDrawer(scale=height / 50, offset=int(height / 5))
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
            data = Image.set_height(data, self.height)
            data = self.id_drawer.draw(index + 1, data)
            previews.append(data)

        return numpy.concatenate(previews, axis=1)
