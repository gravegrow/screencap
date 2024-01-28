import rich.console
from rich import prompt

from screencap.capture import WindowCapture
from screencap.pids.manager import PidManager
from screencap.previews import Previews

console = rich.console.Console()


def main():
    pids = PidManager("Navigator")
    previews = Previews(pids.pids, 360).start()
    pid = pids.select()
    previews.stop()

    capture = WindowCapture(pid).show(720).start()

    try:
        prompt.Prompt.ask("[red bold]Press [green]'ENTER' [red]to exit")
    except KeyboardInterrupt:
        pass

    capture.stop()


if __name__ == "__main__":
    main()
