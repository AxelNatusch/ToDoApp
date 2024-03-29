from abc import ABC, abstractmethod
from typing import Any, List


class DatabaseInterface(ABC):
    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def disconnect(self):
        pass

    @abstractmethod
    def execute(self, operation: Any, parameters: List[Any] | None = None) -> Any:
        pass

    @abstractmethod
    def transaction(self):
        pass

    @abstractmethod
    def commit(self):
        pass

    @abstractmethod
    def rollback(self):
        pass
