import threading

import cv2
from rich import console

from screencap.capture import WindowCapture
from screencap.image_view import ImageView
from screencap.pids import PidManager
from screencap.previews import Previews


def main():
    image_view = ImageView().start()

    pid_manager = PidManager("Navigator")

    previews = Previews()
    previews.start(pid_manager.pids)

    image_view.watch("Preview", previews)

    pid = pid_manager.select_pid()

    previews.stop()

    capture = WindowCapture(pid)
    # capture.set_size(1280, 720)

    console.Console().print("Press 'Q' to exit.")

    while True:
        capture.run()
        capture.show()

        if cv2.waitKey(1) == ord("q"):
            cv2.destroyAllWindows()
            break


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, SystemExit) as e:
        raise SystemExit from e
