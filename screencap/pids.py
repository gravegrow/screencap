import subprocess
from typing import List

from rich import box
from rich.console import Console
from rich.prompt import IntPrompt
from rich.table import Table

console = Console()


def select_pid(process: str) -> str:
    try:
        pids = find_pids(process)
    except subprocess.CalledProcessError as e:
        console.log(f"[red]Process named [bold green]'{process}' [red]not found.")
        raise SystemExit from e

    table = Table(box=box.ROUNDED, header_style="green dim")
    table.add_column("Index", justify="center", style="blue dim", width=len("Index"))
    table.add_column("PID", justify="center", style="dim", width=12)

    for index, pid in enumerate(pids):
        table.add_row(str(index + 1), str(pid))

    console.print(table)

    try:
        choice = IntPrompt.ask("Pick", choices=[str(i + 1) for i in range(len(pids))])
    except KeyboardInterrupt as e:
        raise SystemExit from e

    return pids[int(choice) - 1]


def find_pids(process: str) -> List[str]:
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
