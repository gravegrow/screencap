from screencap.pids.manager import PidManager
from screencap.previews import Previews


def select(process: str) -> str:
    pids = PidManager(process)
    previews = Previews(pids.pids)
    previews.start()

    pid = pids.select()
    previews.terminate()
    return pid
