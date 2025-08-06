from src.domain.entities.stages.raw_data import RawData
from src.domain.entities.stages.predicted_data import PredictedData

from src.domain.interfaces.strategies.i_data_cleaner import IDataCleaner
from src.domain.interfaces.strategies.i_data_selector import IDataSelector
from src.domain.interfaces.strategies.i_data_adapter import IDataAdapter
from src.domain.interfaces.strategies.i_model import IModel

from src.application.bypasses.data_cleaner_bypass import DataCleanerBypass
from src.application.bypasses.data_selector_bypass import DataSelectorBypass
from src.application.bypasses.data_adapter_bypass import DataAdapterBypass
from src.application.bypasses.model_bypass import ModelBypass

class End2EndPredictionFlow:
    """
    Application use case for executing prediction using a trained model
    and an associated data adapter for transformation.
    """

    def __init__(
        self,        
        cleaner: IDataCleaner = None,
        selector: IDataSelector = None,
        adapter: IDataAdapter = None,
        model: IModel = None
    ) -> None:
        
        self.cleaner = cleaner or DataCleanerBypass()
        self.selector = selector or DataSelectorBypass()
        self.adapter = adapter or DataAdapterBypass()
        self.model = model or ModelBypass()

    def execute(self, data: RawData) -> PredictedData:
        """
        Transforms raw data, makes prediction, and reverses transformation.

        Args:
            data (RawData): Raw input data from upstream process.

        Returns:
            PredictedData: Final transformed prediction.
        """
        
        cleaned_data = self.cleaner.clean(data)
        selected_data = self.selector.select(cleaned_data)
        input_data = self.adapter.transform(selected_data)
        output_data = self.model.predict(input_data)
        predicted_data = self.adapter.inverse_transform(output_data)

        return predicted_data
