from src.domain.entities.stages.raw_data import RawData
from src.domain.entities.stages.cleaned_data import CleanedData

from domain.interfaces.strategies.i_feature_cleaner import IFeatureCleaner


class CleanData:
    def __init__(self, cleaner: IFeatureCleaner):
        self.cleaner = cleaner

    def execute(self, data: RawData) -> CleanedData:
        metadata = self.cleaner.fit(self, data)
        return self.cleaner.clean(data)  # -> CleanedData:
