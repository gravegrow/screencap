import threading
from typing import List, Self

import cv2
import numpy as np

from screencap.capture import WindowCapture
from screencap.image import Image
from screencap.image_view import ImageProvider


class Previews(ImageProvider):
    _captures: List[WindowCapture] = []

    is_running: bool = False
    thread: threading.Thread

    def start(self, pids: List[str], height: int = 240):
        self._captures = []

        for pid in pids:
            capture = WindowCapture(pid)
            capture.set_max_height(height)
            self._captures.append(capture)

        self.is_running = True

        self.thread = threading.Thread(target=self._execute)
        self.thread.start()

    def stop(self) -> Self:
        self.is_running = False
        self.thread.join()

        return self

    def _execute(self) -> None:
        lock = threading.Lock()
        with lock:
            while self.is_running:
                images = []
                for index, capture in enumerate(self._captures):
                    capture.run()
                    capture.image.draw_id(index + 1)
                    images.append(capture.image.image)

                if any(img is None for img in images):
                    continue

                self.image.image = np.concatenate(images, axis=1)
                # self.preview.show("Previews")

                if cv2.waitKey(1) == ord("q"):
                    self.stop()
                    break

            # cv2.destroyWindow("Previews")
