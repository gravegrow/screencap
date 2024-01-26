from abc import ABC, abstractmethod
from multiprocessing import Lock, Process
from typing import Self


class Processor(ABC):
    process: Process
    is_running: bool = False
    lock = Lock()

    def start(self) -> Self:
        self.is_running = True
        self.process = Process(target=self.run)
        self.process.start()
        return self

    def stop(self) -> None:
        self.is_running = False
        self.process.terminate()

    @abstractmethod
    def run(self) -> None:
        ...
