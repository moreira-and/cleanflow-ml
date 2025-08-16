from abc import ABC, abstractmethod
from typing import Any, Mapping, List


class IQuery(ABC):
    @abstractmethod
    def get_by_id(self, ids: list[str]) -> Mapping[str, Any]:
        pass

    @abstractmethod
    def list_all(self) -> List[Any]:
        pass
