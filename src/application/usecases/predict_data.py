from src.domain.entities.stages.selected_data import SelectedData
from src.domain.entities.stages.predicted_data import PredictedData

from src.domain.interfaces.strategies.i_model import IModel
from domain.interfaces.strategies.i_model_adapter import IModelAdapter


class PredictData:
    """
    Application use case for executing prediction using a trained model
    and an associated data adapter for transformation.
    """

    def __init__(self, adapter: IModelAdapter, model: IModel) -> None:
        self.adapter = adapter
        self.model = model

    def execute(self, data: SelectedData) -> PredictedData:
        """
        Transforms raw data, makes prediction, and reverses transformation.

        Args:
            data (SelectedData): Raw input data from upstream process.

        Returns:
            PredictedData: Final transformed prediction.
        """
        input_data = self.adapter.transform(data)
        output_data = self.model.predict(input_data)
        predicted_data = self.adapter.inverse_transform(output_data)

        return predicted_data
