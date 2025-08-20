from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict
from src.domain.entities.stages.predicted_data import PredictedData


@dataclass(frozen=True)
class EvaluationConfig:
    """
    Configuration parameters, thresholds, or metadata derived from cleaned data
    that guide evaluation logic.

    Examples include feature importance scores, rankings, variance thresholds,
    or selected column names.
    """

    details: Dict[str, Any] = None


@dataclass(frozen=True)
class EvaluationSummary:
    """
    Result of an evaluation step, capturing both the configuration applied
    and the observations obtained during evaluation.

    Attributes:
        config: The EvaluationConfig that was applied.
        observations: Dictionary of observations (e.g., dropped features, explained variance,
                      or reasons for certain decisions).
    """

    config: EvaluationConfig
    observations: Dict[str, Any]


class IModelEvaluator(ABC):
    """
    Domain-level interface for model evaluation strategies.

    Implementations should be stateless. The 'evaluate' method computes metrics or applies
    evaluation logic based on a prepared configuration and produces a summary of results.
    """

    @abstractmethod
    def evaluate(
        self, data: PredictedData, config: EvaluationConfig
    ) -> EvaluationSummary:
        """
        Apply evaluation logic to the given predicted data according to a previously prepared configuration.

        Args:
            data: PredictedData instance to evaluate.
            config: EvaluationConfig produced by prior preparation steps.

        Returns:
            EvaluationSummary: encapsulates the configuration used and observations collected
                               during evaluation.
        """
        pass
