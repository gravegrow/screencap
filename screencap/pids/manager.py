import subprocess
from typing import List

from screencap.pids.selection_ui import SelectionUI


class PidManager:
    @property
    def pids(self) -> List[str]:
        return self._pids

    def __init__(self, process: str):
        self._pids = self.find_pids(process)
        self._unused = self._pids.copy()

    def select(self, unused: bool = False) -> str:
        pids = self._pids if not unused else self._unused
        SelectionUI.print(pids)
        choice = SelectionUI.ask(pids)

        pid = pids[int(choice) - 1]
        self._unused.remove(pid)

        return pid

    def find_pids(self, process: str) -> List[str]:
        found = subprocess.check_output(
            ["xdotool", "search", "--onlyvisible", "--classname", process],
            text=True,
        )

        pids = []
        for pid in found.split("\n"):
            if pid:
                pids.append(pid)

        return pids

    _pids: List[str]
    _unused: List[str]
