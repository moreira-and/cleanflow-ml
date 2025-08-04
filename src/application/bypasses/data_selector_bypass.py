from src.domain.entities.data.raw_data import RawData
from src.domain.entities.data.selected_data import SelectedData
from src.domain.interfaces.strategies.i_data_selector import IDataSelector


class DataSelectorBypass(IDataSelector):
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
