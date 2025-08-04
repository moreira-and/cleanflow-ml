from src.domain.entities.data.selected_data import SelectedData
from domain.entities.data.model_input_data import ModelInputData
from domain.entities.data.model_output_data import ModelOutputData
from domain.entities.data.predicted_data import PredictedData

from abc import ABC, abstractmethod

class IDataAdapter(ABC):
    """
    Interface for adapting domain data to model-ready formats and vice versa.

    This abstraction defines the contract for preprocessing and postprocessing steps
    that map between business-level data representations and model input/output formats.
    It enables separation of concerns by isolating transformation logic from orchestration
    and model implementation, promoting reusability and testability.

    Typical responsibilities include:
    - Feature scaling, encoding, and normalization before model training or inference.
    - Reconstructing predictions into domain-relevant representations for reporting
      or downstream processing.

    Methods:
        fit(data: SelectedData) -> None:
            Learns transformation parameters (e.g., scalers, encoders) from selected data.

        transform(data: SelectedData) -> ModelInputData:
            Applies transformations to convert domain data into model-compatible input.

        inverse_transform(data: ModelOutputData) -> PredictedData:
            Converts model outputs back into a domain-level predicted structure.
    """

    @abstractmethod
    def fit(self, data: SelectedData) -> None:
        """
        Fit transformation logic to the selected data, storing any parameters
        needed for consistent transformation and inversion.

        Args:
            data (SelectedData): Cleaned and selected dataset used to compute
                                 transformation parameters (e.g., min/max, mean/std).
        """
        pass

    @abstractmethod
    def transform(self, data: SelectedData) -> ModelInputData:
        """
        Apply the fitted transformation to selected domain data, preparing
        it for model consumption.

        Args:
            data (SelectedData): Structured input data from the domain layer.

        Returns:
            ModelInputData: Transformed data in a format suitable for training or inference.
        """
        pass

    @abstractmethod
    def inverse_transform(self, data: ModelOutputData) -> PredictedData:
        """
        Reverse the transformation on model output to return domain-level predictions.

        Args:
            data (ModelOutputData): Output from the model, typically scaled or encoded.

        Returns:
            PredictedData: Human-readable or business-relevant prediction results.
        """
        pass
