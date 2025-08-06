from src.domain.entities.stages.selected_data import SelectedData
from src.domain.entities.stages.model_input_data import ModelInputData
from src.domain.entities.stages.model_output_data import ModelOutputData
from src.domain.entities.stages.predicted_data import PredictedData
from src.domain.interfaces.strategies.i_data_adapter import IDataAdapter


class DataAdapterBypass(IDataAdapter):
    """
    A jumper/mock implementation of IDataAdapter.
    Useful for testing, composition, or bypassing selection logic in pipelines.
    """

    def fit(self, data: SelectedData) -> None:
        # Mock metadata output
        pass

    def transform(self, data: SelectedData) -> ModelInputData:
        return ModelInputData(data.data)

    def inverse_transform(self, data: ModelOutputData) -> PredictedData:
        return PredictedData(data.data)