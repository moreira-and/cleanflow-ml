from abc import ABC, abstractmethod
from src.domain.entities.base import BaseDataEntity


class IFeatureLoader(ABC):
    @abstractmethod
    def load(self, path_url: str) -> BaseDataEntity:
        pass
