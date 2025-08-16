from abc import ABC, abstractmethod
from src.domain.entities.stages.raw_data import RawData
from src.domain.entities.stages.cleaned_data import CleanedData
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class CleaningConfig:
    """
    Parameters or thresholds extracted from raw data that drive cleaning logic.
    """


@dataclass(frozen=True)
class CleaningSummary:
    config: CleaningConfig
    issues: dict[str, Any]  # e.g., missing rates, outliers detected


class IDataCleaner(ABC):
    """
    Domain-level contract for data cleaning strategies.
    """

    @abstractmethod
    def prepare(self, data: RawData) -> CleaningSummary:
        """
        Inspect the raw data, extract cleaning parameters, detect issues, and
        return a summary including a concrete config for cleaning.
        """
        pass

    @abstractmethod
    def clean(self, data: RawData, config: CleaningConfig) -> CleanedData:
        """
        Apply cleaning logic based on a previously prepared config.
        """
        pass
