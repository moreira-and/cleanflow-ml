from src.domain.entities.stages.raw_data import RawData
from src.domain.entities.stages.cleaned_data import CleanedData
from domain.interfaces.strategies.i_feature_cleaner import IFeatureCleaner


class DataCleanerBypass(IFeatureCleaner):
    """
    A jumper/mock implementation of IDataCleaner.
    Useful for testing, composition, or bypassing selection logic in pipelines.
    """

    def fit(self, data: RawData) -> None:
        # Mock metadata output
        pass

    def clean(self, data: RawData) -> CleanedData:
        CleanedData(data.data)
