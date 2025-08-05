import pytest
from src.domain.interfaces.strategies import IDataAdapter
from src.domain.entities.data.selected_data import SelectedData
from domain.entities.data.model_input_data import ModelInputData
from domain.entities.data.model_output_data import ModelOutputData
from domain.entities.data.predicted_data import PredictedData

class DummySelectedData(SelectedData):
    pass

class DummyModelInputData(ModelInputData):
    pass

class DummyModelOutputData(ModelOutputData):
    pass

class DummyPredictedData(PredictedData):
    pass

class DummyAdapter(IDataAdapter):
    def fit(self, data: SelectedData) -> None:
        self.fitted = True

    def transform(self, data: SelectedData) -> ModelInputData:
        if not hasattr(self, "fitted"):
            raise RuntimeError("Must call fit() before transform()")
        return DummyModelInputData(data=[], metadata={}, schema=None)

    def inverse_transform(self, data: ModelOutputData) -> PredictedData:
        if not hasattr(self, "fitted"):
            raise RuntimeError("Must call fit() before inverse_transform()")
        return DummyPredictedData(data=[], metadata={}, schema=None)

def test_cannot_instantiate_interface():
    with pytest.raises(TypeError):
        IDataAdapter()

def test_dummy_adapter_implements_interface():
    adapter = DummyAdapter()
    dummy_data = DummySelectedData(data=[], metadata={}, schema=None)
    dummy_model_output = DummyModelOutputData(data=[], metadata={}, schema=None)

    adapter.fit(dummy_data)
    assert hasattr(adapter, "fitted")

    model_input = adapter.transform(dummy_data)
    assert isinstance(model_input, ModelInputData)

    predicted = adapter.inverse_transform(dummy_model_output)
    assert isinstance(predicted, PredictedData)
