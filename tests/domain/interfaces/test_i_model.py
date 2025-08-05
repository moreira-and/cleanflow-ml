import pytest
from src.domain.interfaces.strategies import IModel
from src.domain.entities.data.model_input_data import ModelInputData
from src.domain.entities.data.model_output_data import ModelOutputData
from src.domain.enums.problem_type import ProblemType

class DummyModelInputData(ModelInputData):
    pass

class DummyModelOutputData(ModelOutputData):
    pass

class DummyModel(IModel):
    def train(self, problem_type: ProblemType, data: ModelInputData) -> None:
        self.trained = True
        self.problem_type = problem_type
        self.data = data

    def predict(self, data: ModelInputData) -> ModelOutputData:
        if not getattr(self, "trained", False):
            raise RuntimeError("Model not trained")
        return DummyModelOutputData(data=[], metadata={}, schema=None)

def test_cannot_instantiate_interface():
    with pytest.raises(TypeError):
        IModel()

def test_dummy_model_implements_interface():
    model = DummyModel()
    dummy_input = DummyModelInputData(data=[], metadata={}, schema=None)

    model.train(ProblemType.CLASSIFICATION, dummy_input)
    assert model.trained
    assert model.problem_type == ProblemType.CLASSIFICATION
    assert model.data == dummy_input

    output = model.predict(dummy_input)
    assert isinstance(output, ModelOutputData)
