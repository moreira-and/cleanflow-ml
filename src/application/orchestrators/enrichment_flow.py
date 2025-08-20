from src.domain.entities.stages.raw_data import RawData
from src.domain.entities.stages.selected_data import SelectedData

from domain.interfaces.strategies.i_feature_cleaner import IFeatureCleaner
from domain.interfaces.strategies.i_feature_selector import IFeatureSelector

from src.application.bypasses.data_cleaner_bypass import DataCleanerBypass
from src.application.bypasses.data_selector_bypass import DataSelectorBypass


class EnrichmentFlow:
    """
    Application use case for executing prediction using a trained model
    and an associated data adapter for transformation.
    """

    def __init__(
        self, cleaner: IFeatureCleaner = None, selector: IFeatureSelector = None
    ) -> None:
        self.cleaner = cleaner or DataCleanerBypass()
        self.selector = selector or DataSelectorBypass()

    def execute(self, data: RawData) -> SelectedData:
        """
        Transforms raw data and makes selections.

        Args:
            data (RawData): Raw input data from upstream process.

        Returns:
            SelectedData: Selected data.
        """

        cleaned_data = self.cleaner.clean(data)
        selected_data = self.selector.select(cleaned_data)

        return selected_data
