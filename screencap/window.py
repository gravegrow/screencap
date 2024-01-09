import subprocess
from dataclasses import dataclass, field
from typing import List

from rich import box, console, prompt, table, traceback

from screencap.geometry import WindowGeometry

traceback.install(max_frames=1)


@dataclass
class Window:
    process: str

    @property
    def geometry(self):
        return self._get_geometry(self._pid)

    def choose(self):
        pids = self._find_pids()
        self._pid = self._choose_pid(pids)

    def _get_geometry(self, pid: str):
        try:
            out = subprocess.check_output(["xdotool", "getwindowgeometry", pid], text=True)
        except subprocess.CalledProcessError as e:
            console.Console().log(f"Process '{self.process} was terminated.")
            raise e.with_traceback(None)

        out = out.split()

        x, y = out[3].split(",")
        width, height = out[7].split("x")

        self._geometry.x = int(x)
        self._geometry.y = int(y)
        self._geometry.width = int(width)
        self._geometry.height = int(height)

        return self._geometry

    def _choose_pid(self, pids: List[str]) -> str:
        tbl = table.Table(box=box.ROUNDED, header_style="green dim")
        tbl.add_column("Index", justify="center", style="blue dim", width=len("Index"))
        tbl.add_column("PID", justify="center", style="dim", width=12)

        for index, pid in enumerate(pids):
            tbl.add_row(str(index + 1), str(pid))

        console.Console().print(tbl)
        choice = prompt.IntPrompt.ask("Pick", choices=[str(i + 1) for i in range(len(pids))])

        return pids[int(choice) - 1]

    def _find_pids(self) -> List[str]:
        try:
            found = subprocess.check_output(
                [
                    "xdotool",
                    "search",
                    "--onlyvisible",
                    "--classname",
                    self.process,
                ],
                text=True,
            )
        except subprocess.CalledProcessError as e:
            console.Console().log(f"Process '{self.process}' not found.")
            raise e

        pids = []
        for pid in found.split("\n"):
            if pid:
                pids.append(pid)

        return pids

    _pid: str = field(init=False)
    _geometry: WindowGeometry = field(init=False)

    def __post_init__(self):
        self._geometry = WindowGeometry(0, 0, 20, 20)
