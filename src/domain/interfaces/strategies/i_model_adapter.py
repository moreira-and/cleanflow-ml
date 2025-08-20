from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict

from src.domain.entities.stages.selected_data import SelectedData
from src.domain.entities.stages.model_input_data import ModelInputData
from src.domain.entities.stages.model_output_data import ModelOutputData
from src.domain.entities.stages.predicted_data import PredictedData


@dataclass(frozen=True)
class TransformationConfig:
    """
    Parameters learned or derived from selected data to drive forward transformation.
    Examples: scaling factors, encoding maps, feature order, normalization statistics.
    """

    params: Dict[str, Any]


@dataclass(frozen=True)
class TransformationSummary:
    """
    Outcome of preparing the forward transformation.
    Contains the config and observations (e.g., which features were dropped/encoded).
    """

    config: TransformationConfig
    observations: Dict[str, Any]


@dataclass(frozen=True)
class InverseConfig:
    """
    Parameters derived from model output structure to guide inverse transformation.
    Examples: output schema mapping, decoding rules, target scaling reversal.
    """

    params: Dict[str, Any]


@dataclass(frozen=True)
class InverseSummary:
    """
    Outcome of preparing the inverse transformation.
    """

    config: InverseConfig
    observations: Dict[str, Any]


class IModelAdapter(ABC):
    """
    Domain contract for mapping between selected domain data and model I/O,
    using explicit prepare → apply steps both forward (transform) and backward
    (inverse_transform).
    """

    @abstractmethod
    def prepare_transform(self, data: SelectedData) -> TransformationSummary:
        """
        Inspect selected data to derive transformation parameters (e.g., compute
        scaling, encoding, feature ordering) and return a summary with config.
        """
        pass

    @abstractmethod
    def transform(
        self, data: SelectedData, config: TransformationConfig
    ) -> ModelInputData:
        """
        Apply forward transformation using a previously prepared config.
        """
        pass

    @abstractmethod
    def prepare_inverse(self, output: ModelOutputData) -> InverseSummary:
        """
        Inspect raw model output to derive inverse transformation parameters,
        such as decoding maps or rescaling factors.
        """
        pass

    @abstractmethod
    def inverse_transform(
        self, data: ModelOutputData, config: InverseConfig
    ) -> PredictedData:
        """
        Apply inverse transformation using a previously prepared inverse config.
        """
        pass
