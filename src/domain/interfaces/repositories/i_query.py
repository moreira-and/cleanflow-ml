from abc import ABC, abstractmethod
from typing import List, Any


class IQuery(ABC):
    @abstractmethod
    def get_by_id(self, id: str) -> Any:
        pass

    @abstractmethod
    def list_all(self) -> List[Any]:
        pass
