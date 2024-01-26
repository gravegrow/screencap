from rich import box
from rich.console import Console
from rich.prompt import IntPrompt
from rich.table import Table

console = Console()


class SelectionUI:
    @staticmethod
    def print(pids):
        table = Table(box=box.ROUNDED, header_style="green dim")
        table.add_column("Index", justify="center", style="blue dim", width=len("Index"))
        table.add_column("PID", justify="center", style="dim", width=12)

        for index, pid in enumerate(pids):
            table.add_row(str(index + 1), str(pid))

        console.print(table)

    @staticmethod
    def ask(pids):
        return IntPrompt.ask("Pick", choices=[str(i + 1) for i in range(len(pids))])
