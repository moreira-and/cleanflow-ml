from src.domain.entities.stages.raw_data import RawData
from src.domain.entities.stages.cleaned_data import CleanedData
from src.domain.interfaces.strategies.i_data_cleaner import IDataCleaner


class DataCleanerBypass(IDataCleaner):
    """
    A jumper/mock implementation of IDataCleaner.
    Useful for testing, composition, or bypassing selection logic in pipelines.
    """

    def fit(self, data: RawData) -> None:
        # Mock metadata output
        pass

    def clean(self, data: RawData) -> CleanedData:
        CleanedData(data.data)