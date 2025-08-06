from src.domain.entities.stages.model_input_data import ModelInputData
from src.domain.entities.stages.model_output_data import ModelOutputData
from src.domain.interfaces.strategies.i_model import IModel


class ModelBypass(IModel):
    """
    A jumper/mock implementation of IModel.
    Useful for testing, composition, or bypassing selection logic in pipelines.
    """

    def train(self, data: ModelInputData) -> None:
        # Mock metadata output
        pass

    def predict(self, data: ModelInputData) -> ModelOutputData:
        return ModelOutputData(data.data)
