from abc import ABC, abstractmethod
from threading import Lock, Thread
from typing import Self


class Threaded(ABC):
    thread: Thread
    lock: Lock = Lock()
    is_running: bool = False

    def start(self) -> Self:
        self.is_running = True
        self.thread = Thread(target=self.run)
        self.thread.start()
        return self

    def stop(self) -> None:
        self.is_running = False

    @abstractmethod
    def run(self) -> None:
        ...
