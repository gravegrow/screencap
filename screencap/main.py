import cv2
from rich import console

from screencap.capture import WindowCapture


def main():
    capture = WindowCapture("gl")
    capture.set_size(1280, 720)
    capture.start()

    console.Console().print("Press 'Q' to exit.")

    while capture.is_running:
        capture.show()
        # capture.image.crop((10, 10, 50, 50)).show("name")

        if cv2.waitKey(1) == ord("q"):
            cv2.destroyAllWindows()
            capture.stop()
            break


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, SystemExit) as e:
        raise SystemExit from e
