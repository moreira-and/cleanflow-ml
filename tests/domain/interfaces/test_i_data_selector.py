import pytest
from src.domain.interfaces.strategies import IDataSelector
from src.domain.entities.data.cleaned_data import CleanedData
from src.domain.entities.data.selected_data import SelectedData

# Dummy classes para teste
class DummyCleanedData(CleanedData):
    pass

class DummySelectedData(SelectedData):
    pass

# Dummy implementação da interface
class DummyDataSelector(IDataSelector):
    def fit(self, data: CleanedData) -> None:
        self.fitted = True

    def select(self, data: CleanedData) -> SelectedData:
        if not hasattr(self, "fitted"):
            raise RuntimeError("Must call fit() before select()")
        return DummySelectedData(data=[], metadata={}, schema=None)

def test_interface_cannot_be_instantiated():
    with pytest.raises(TypeError):
        IDataSelector()  # não pode instanciar abstrata

def test_dummy_implementation_respects_interface():
    selector = DummyDataSelector()
    dummy_data = DummyCleanedData(data=[], metadata={}, schema=None)

    selector.fit(dummy_data)
    assert hasattr(selector, "fitted")

    selected = selector.select(dummy_data)
    assert isinstance(selected, SelectedData)
