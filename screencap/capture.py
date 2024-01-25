from typing import Self

from screencap import pids
from screencap.grabber import WindowGrabber
from screencap.image.image import Image
from screencap.image.viewer import Viewer
from screencap.thread import Threaded


class WindowCapture(Threaded):
    def __init__(self, process: str):
        self.pid = pids.select(process)
        self.grabber = WindowGrabber(self.pid)
        self.viewer = Viewer()
        self.image: Image = Image()
        self._show: bool = False
        self._view_name = f"WindowCapture - PID: {self.pid}"

    def show(self, height: int = 720) -> Self:
        self.viewer.height = height
        self._show = True
        return self

    def run(self):
        while self.is_running:
            with self.lock:
                self.image.data = self.grabber.grab()

                if self._show:
                    self.viewer.view(self._view_name, self.image.data)


def main():
    capture = WindowCapture("Navigator").start()
    capture.show(720)


if __name__ == "__main__":
    main()
