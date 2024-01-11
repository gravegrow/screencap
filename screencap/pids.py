import subprocess
from typing import List

from rich import box
from rich.console import Console
from rich.prompt import IntPrompt
from rich.table import Table

from screencap.utils import keyboard_interrupt

console = Console()


@keyboard_interrupt
def select_pid(process: str) -> str:
    pids = find_pids(process)

    table = Table(box=box.ROUNDED, header_style="green dim")
    table.add_column("Index", justify="center", style="blue dim", width=len("Index"))
    table.add_column("PID", justify="center", style="dim", width=12)

    for index, pid in enumerate(pids):
        table.add_row(str(index + 1), str(pid))

    console.print(table)
    choice = IntPrompt.ask("Pick", choices=[str(i + 1) for i in range(len(pids))])

    return pids[int(choice) - 1]


def find_pids(process: str) -> List[str]:
    try:
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
    except subprocess.CalledProcessError as e:
        console.log(f"[bold red]Process [bold green]'{process}' [bold red]not found.")
        raise SystemExit(e) from e

    pids = []
    for pid in found.split("\n"):
        if pid:
            pids.append(pid)

    return pids


if __name__ == "__main__":
    print(select_pid("Navigator"))
