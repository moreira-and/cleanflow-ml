from src.domain.entities.stages import SelectedData, ModelInputData
from src.domain.interfaces.strategies.i_data_adapter import (
    IDataAdapter,
    TransformationConfig,
)


class AdaptData:
    def __init__(self, adapter: IDataAdapter, config: TransformationConfig = None):
        self.adapter = adapter
        self.config = config

    def execute(self, data: SelectedData) -> ModelInputData:
        return self.adapter.transform(data=data, config=self.config)
