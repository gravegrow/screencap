import subprocess
from dataclasses import dataclass, field

from rich import console

from screencap.geometry import WindowGeometry


@dataclass
class Window:
    pid: str

    @property
    def geometry(self):
        return self._get_geometry(self.pid)

    def _get_geometry(self, pid: str) -> WindowGeometry | None:
        try:
            out = subprocess.check_output(["xdotool", "getwindowgeometry", pid], text=True)
        except subprocess.CalledProcessError as _:
            console.Console().log(f"[bold red]Process PID [bold green]{pid} [bold red]lost.")
            return None

        out = out.split()
        x, y = out[3].split(",")
        width, height = out[7].split("x")

        self._geometry.set_dimensions(int(x), int(y), int(width), int(height))
        return self._geometry

    _geometry: WindowGeometry = field(init=False)

    def __post_init__(self):
        self._geometry = WindowGeometry()
