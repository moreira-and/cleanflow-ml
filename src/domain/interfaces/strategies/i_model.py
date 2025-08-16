from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict
from src.domain.entities.stages.model_input_data import ModelInputData
from src.domain.entities.stages.model_output_data import ModelOutputData
from src.domain.enums.problem_type import ProblemType


@dataclass(frozen=True)
class TrainingConfig:
    """
    Parameters or hyperparameters determined/validated before actual training.
    Examples: learning rate, feature subset, class weights, early stopping thresholds.
    """

    params: Dict[str, Any]


@dataclass(frozen=True)
class TrainingSummary:
    """
    Outcome of preparing the training step: config plus observations such as
    class imbalance, data quality warnings, estimated capacity needs.
    """

    config: TrainingConfig
    observations: Dict[str, Any]


@dataclass(frozen=True)
class PredictionConfig:
    """
    Parameters derived or adjusted before prediction.
    Examples: thresholds for classification, calibration maps, ensemble weights.
    """

    params: Dict[str, Any]


@dataclass(frozen=True)
class PredictionSummary:
    """
    Outcome of preparing inference: config plus diagnostics (e.g., input drift flags,
    expected confidence adjustments).
    """

    config: PredictionConfig
    diagnostics: Dict[str, Any]


class IModel(ABC):
    """
    Domain-level contract for modeling strategies (training + inference) with explicit
    preparation and application phases to avoid hidden state and improve observability.
    """

    @abstractmethod
    def prepare_training(
        self, problem_type: ProblemType, data: ModelInputData
    ) -> TrainingSummary:
        """
        Analyze input data and problem type to derive training config and surface
        any relevant observations before actually fitting the model.
        """
        pass

    @abstractmethod
    def train(
        self, problem_type: ProblemType, data: ModelInputData, config: TrainingConfig
    ) -> None:
        """
        Train or fit the model using the provided config. Implementations may mutate internal
        state (i.e., learned parameters) as a result.
        """
        pass

    @abstractmethod
    def prepare_prediction(self, data: ModelInputData) -> PredictionSummary:
        """
        Inspect the input for inference to derive prediction-time config (e.g., calibration)
        and diagnostics.
        """
        pass

    @abstractmethod
    def predict(
        self, data: ModelInputData, config: PredictionConfig
    ) -> ModelOutputData:
        """
        Perform inference using a precomputed prediction config.
        """
        pass
