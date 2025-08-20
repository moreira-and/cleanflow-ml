from src.domain.entities.stages.raw_data import RawData
from src.domain.entities.stages.selected_data import SelectedData
from domain.interfaces.strategies.i_feature_selector import IFeatureSelector


class DataSelectorBypass(IFeatureSelector):
    """
    A jumper/mock implementation of IDataSelector.
    Useful for testing, composition, or bypassing selection logic in pipelines.
    """

    def fit(self, data: RawData) -> None:
        # Mock metadata output
        pass

    def select(self, data: SelectedData) -> SelectedData:
        # Pass-through — no transformation applied
        return SelectedData(data.data)
