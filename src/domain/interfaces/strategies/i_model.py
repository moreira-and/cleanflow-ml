from src.domain.entities.data.model_input_data import ModelInputData
from src.domain.entities.data.model_output_data import ModelOutputData
from src.domain.enums.problem_type import ProblemType
from abc import ABC, abstractmethod

class IModel(ABC):
    """
    Interface for model training and prediction within the domain layer.

    This abstraction defines the behavior expected from any learning algorithm — statistical or machine learning — 
    employed in the system, ensuring consistent contracts for both training and inference routines.

    Design goals:
    - Decouple orchestration logic (application layer) from concrete implementations (infrastructure layer).
    - Allow transparent replacement of modeling strategies, regardless of the underlying framework or library.
    - Improve testability by enabling mocking or substitution of model behavior in isolation.

    Typical implementations wrap external libraries such as scikit-learn, TensorFlow, or PyTorch, 
    and may range from simple linear models to complex deep learning architectures.

    Methods:
        train(problem_type: ProblemType, data: ModelInputData) -> None
        predict(data: ModelInputData) -> ModelOutputData
    """

    @abstractmethod
    def train(self, problem_type: ProblemType, data: ModelInputData) -> None:
        """
        Trains the model using the specified problem type and structured input data.

        Args:
            problem_type (ProblemType): An enumeration indicating the nature of the task 
                                        (e.g., classification, regression).
            data (ModelInputData): A structured object containing input features, labels, 
                                   and optionally metadata for training.
        """
        pass

    @abstractmethod
    def predict(self, data: ModelInputData) -> ModelOutputData:
        """
        Performs inference using the trained model on new input data.

        Args:
            data (ModelInputData): A structured input containing features required for prediction.

        Returns:
            ModelOutputData: Structured output containing the prediction results, 
                             which may include raw outputs, probabilities, or predicted labels.
        """
        pass