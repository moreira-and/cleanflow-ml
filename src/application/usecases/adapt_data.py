from src.domain.entities.stages import SelectedData, ModelInputData
from domain.interfaces.strategies.i_model_adapter import (
    IModelAdapter,
    TransformationConfig,
)


class AdaptData:
    def __init__(self, adapter: IModelAdapter, config: TransformationConfig = None):
        self.adapter = adapter
        self.config = config

    def execute(self, data: SelectedData) -> ModelInputData:
        return self.adapter.transform(data=data, config=self.config)
