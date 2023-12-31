from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from threading import Lock, Thread


@dataclass
class Threaded(ABC):
    lock: Lock = field(default_factory=Lock, init=False)
    is_runing: bool = field(default_factory=bool, init=False)

    def start(self) -> None:
        self.is_runing = True
        thread = Thread(target=self.run, daemon=True)
        thread.start()

    def stop(self) -> None:
        self.is_runing = False

    def run(self) -> None:
        while self.is_runing:
            with self.lock:
                self._execute()

    @abstractmethod
    def _execute(self):
        ...
