from abc import ABC, abstractmethod
from threading import Lock, Thread


class Threaded(ABC):
    lock: Lock = Lock()
    is_running: bool = False

    def start(self) -> None:
        self.is_running = True
        thread = Thread(target=self.run, daemon=True)
        thread.start()

    def stop(self) -> None:
        self.is_running = False

    def run(self) -> None:
        while self.is_running:
            with self.lock:
                self._execute()

    @abstractmethod
    def _execute(self):
        ...
