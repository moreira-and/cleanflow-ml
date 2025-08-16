# infra/config/yaml_config_provider.py
from __future__ import annotations
from pathlib import Path
from typing import Any, Mapping, Optional
import yaml
import logging

from src.domain.interfaces.repositories import IConfigProvider


class YamlConfigProvider(IConfigProvider):
    """
    YAML implementation of IConfigProvider.
    Can be replaced by any other provider (DB, JSON, Env) without
    changing Application Layer code.
    """

    def __init__(
        self, filepath: str | Path, logger: Optional[logging.Logger] = None
    ) -> None:
        self._filepath = Path(filepath)
        self._config: Optional[Mapping[str, Any]] = None
        self._log = logger or logging.getLogger(self.__class__.__name__)

    def load(self) -> Mapping[str, Any]:
        """
        Load YAML file into memory.
        """
        if self._config is None:
            if not self._filepath.exists():
                raise FileNotFoundError(f"YAML file not found: {self._filepath}")
            with self._filepath.open("r", encoding="utf-8") as f:
                self._config = yaml.safe_load(f)
        return self._config

    def get(self, key: str, default: Any = None) -> Any:
        """
        Retrieve a value from the YAML configuration using dot notation.
        """
        if self._config is None:
            self.load()

        keys = key.split(".")
        value: Any = self._config
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        return value
