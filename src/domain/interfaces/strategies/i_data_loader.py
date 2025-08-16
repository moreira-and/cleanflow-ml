from abc import ABC, abstractmethod
from src.domain.entities.base import BaseDataEntity


class IDataLoader(ABC):
    @abstractmethod
    def load(self, path_url: str) -> BaseDataEntity:
        pass
