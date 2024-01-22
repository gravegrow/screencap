import subprocess
from typing import List

from rich import box
from rich.console import Console
from rich.prompt import IntPrompt
from rich.table import Table
from signals import Signal

console = Console()


class PidHandler:
    selection_performed: Signal = Signal()

    @property
    def pids(self) -> List[str]:
        return self._pids

    def __init__(self, process: str):
        self._pids = self.find_pids(process)

    def select_pid(self) -> str:
        table = Table(box=box.ROUNDED, header_style="green dim")
        table.add_column("Index", justify="center", style="blue dim", width=len("Index"))
        table.add_column("PID", justify="center", style="dim", width=12)

        for index, pid in enumerate(self._pids):
            table.add_row(str(index + 1), str(pid))

        console.print(table)

        try:
            choice = IntPrompt.ask("Pick", choices=[str(i + 1) for i in range(len(self._pids))])
        except KeyboardInterrupt as e:
            raise SystemExit from e

        self.selection_performed.emit()
        return self._pids[int(choice) - 1]

    def find_pids(self, process: str) -> List[str]:
        found = subprocess.check_output(
            [
                "xdotool",
                "search",
                "--onlyvisible",
                "--classname",
                process,
            ],
            text=True,
        )

        pids = []
        for pid in found.split("\n"):
            if pid:
                pids.append(pid)

        return pids

    _pids: List[str]
