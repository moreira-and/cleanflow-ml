from abc import ABC, abstractmethod
from typing import Any, Dict, Union
from src.domain.entities.stages.predicted_data import PredictedData


class IModelTransparency(ABC):
    """
    Domain-level contract for model explainability or transparency.

    Implementations must be stateless and backend-agnostic.
    Methods should provide feature-level explanations or global importance
    without assuming specific data types.
    """

    @abstractmethod
    def feature_importances(self, model: Any, data: PredictedData) -> Dict[str, float]:
        """
        Returns a dictionary mapping feature names to importance scores.

        Args:
            model: Trained model object (supports predict or equivalent)
            data: PredictedData instance containing features used by the model

        Returns:
            Dict[str, float]: feature importance scores
        """
        pass

    @abstractmethod
    def local_explanations(
        self, model: Any, data: PredictedData
    ) -> Union[Dict[int, Dict[str, float]], Any]:
        """
        Returns local explanations per instance, e.g., SHAP values.

        Args:
            model: Trained model
            data: PredictedData instance

        Returns:
            Dict[int, Dict[str, float]] or backend-specific object:
                - Key: row index
                - Value: feature contributions for that instance
        """
        pass
