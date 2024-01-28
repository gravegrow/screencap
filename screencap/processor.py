from abc import ABC, abstractmethod
from multiprocessing import Lock, Process, Queue
from typing import Any, Dict, Self


class Processor(ABC):
    process: Process
    is_running: bool = False
    lock = Lock()

    _queue = Queue()
    _shared: Dict = {}

    def share(self, key: str, value: Any) -> Self:
        self._shared = self._queue.get()
        self._shared[key] = value
        self._queue.put(self._shared)
        return self

    def get_shared(self, key: str) -> Any:
        self._shared = self._queue.get()
        self._queue.put(self._shared)
        return self._shared[key]

    def start(self) -> Self:
        self._queue.put(self._shared)

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
