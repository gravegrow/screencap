import subprocess
import tkinter
from dataclasses import dataclass, field
from typing import List, Tuple

from rich import box
from rich.console import Console
from rich.prompt import IntPrompt
from rich.table import Table

console = Console()
prompt = IntPrompt()


@dataclass
class Geometry:
    x: int
    y: int
    width: int
    height: int

    @property
    def x_bounds(self):
        return min(self.x + self.width, self._root.winfo_screenwidth())

    @property
    def y_bounds(self):
        return min(self.y + self.height, self._root.winfo_screenheight())

    @property
    def region(self) -> Tuple[int, int, int, int]:
        return self.x, self.y, self.x_bounds, self.y_bounds

    _root: tkinter.Tk = field(init=False, default_factory=tkinter.Tk)


@dataclass
class Window:
    process: str
    _pid: str = field(init=False)

    @property
    def geometry(self):
        return self._get_geometry(self._pid)

    def __post_init__(self):
        self._pid = self._pick_pid()

    def _get_geometry(self, pid: str):
        out = subprocess.check_output(["xdotool", "getwindowgeometry", str(pid)], text=True)
        out = out.split()

        x, y = out[3].split(",")
        width, height = out[7].split("x")

        return Geometry(int(x), int(y), int(width), int(height))

    def _pick_pid(self) -> str:
        pids = self._find_pids()

        table = Table(box=box.ROUNDED, header_style="green dim")
        table.add_column("Index", justify="center", style="blue dim", width=len("Index"))
        table.add_column("PID", justify="center", style="dim", width=12)

        for index, pid in enumerate(pids):
            table.add_row(str(index + 1), str(pid))

        console.print(table)
        choice = prompt.ask("Pick", choices=[str(i + 1) for i in range(len(pids))])

        return pids[int(choice) - 1]

    def _find_pids(self) -> List[str]:
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

        pids = []
        for pid in found.split("\n"):
            if pid:
                pids.append(pid)

        return pids


if __name__ == "__main__":
    window = Window("Wow.exe")
    print(window.geometry)
