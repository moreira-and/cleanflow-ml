from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict
from src.domain.entities.stages.cleaned_data import CleanedData
from src.domain.entities.stages.selected_data import SelectedData


@dataclass(frozen=True)
class SelectionConfig:
    """
    Parameters, thresholds or metadata derived from cleaned data that drive selection logic.
    Examples: importance scores, feature rankings, variance thresholds, selected column names.
    """

    details: Dict[str, Any] = None


@dataclass(frozen=True)
class SelectionSummary:
    """
    Outcome of the preparation step: the config to apply plus what was observed.
    """

    config: SelectionConfig
    observations: Dict[str, Any]  # e.g., dropped features, variance explained, reasons


class IDataSelector(ABC):
    """
    Domain-level contract for feature/record selection strategies.
    Stateless implementations should compute config in prepare and consume it in select.
    """

    @abstractmethod
    def prepare(self, data: CleanedData) -> SelectionSummary:
        """
        Analyze cleaned data to derive selection parameters and record observations.

        Returns:
            SelectionSummary: includes the concrete config and what was seen (e.g., candidate features).
        """
        pass

    @abstractmethod
    def select(self, data: CleanedData, config: SelectionConfig) -> SelectedData:
        """
        Apply selection logic based on a previously prepared config.

        Args:
            data: CleanedData to select from.
            config: SelectionConfig produced by prepare.

        Returns:
            SelectedData: subset or transformed version after selection.
        """
        pass
