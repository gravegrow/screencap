import cv2
from rich import console

from screencap.capture import WindowCapture
from screencap.pids import PidHandler
from screencap.previews import Previews


def main():
    pid_handler = PidHandler("Navigator")

    previews = Previews(pid_handler.pids)
    previews.start()
    pid_handler.selection_performed.connect(previews.stop)

    pid = pid_handler.select_pid()

    capture = WindowCapture(pid)
    capture.set_size(1280, 720)
    capture.start()

    console.Console().print("Press 'Q' to exit.")

    while capture.is_running:
        capture.show()

        if cv2.waitKey(1) == ord("q"):
            cv2.destroyAllWindows()
            capture.stop()
            break


if __name__ == "__main__":
    main()
    # try:
    # except (KeyboardInterrupt, SystemExit) as e:
    #     raise SystemExit from e
