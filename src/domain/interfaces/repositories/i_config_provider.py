from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, Optional


class IConfigProvider(ABC):
    """
    Interface for configuration providers.
    Application Layer depends only on this contract.
    """

    @abstractmethod
    def get(self, key: str, default: Optional[Any] = None) -> Any:
        """
        Retrieve a configuration value by key.
        Supports nested keys using dot notation.
        """
        pass

    @abstractmethod
    def load(self) -> None:
        """
        load the configuration (optional for dynamic sources).
        """
        pass

    def reload(self) -> None:
        """
        Force reload of YAML file.
        """
        self._config = None
        self.load()
