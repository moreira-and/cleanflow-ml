from abc import ABC, abstractmethod
from typing import Any


class ICommand(ABC):
    @abstractmethod
    def save(self, to_save: Any) -> None:
        pass

    @abstractmethod
    def delete(self, id: str) -> None:
        pass

    @abstractmethod
    def edit(self, id: str) -> None:
        pass
