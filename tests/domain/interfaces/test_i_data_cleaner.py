import pytest
from src.domain.interfaces.strategies import IDataCleaner
from src.domain.entities.data import RawData, CleanedData

# Dummy implementations só pra teste
class DummyRawData(RawData):
    pass

class DummyCleanedData(CleanedData):
    pass

# Implementação de teste da interface
class DummyDataCleaner(IDataCleaner):
    def fit(self, data: RawData) -> None:
        self.fitted = True

    def clean(self, data: RawData) -> CleanedData:
        if not hasattr(self, "fitted"):
            raise RuntimeError("Must call fit() before clean()")
        return DummyCleanedData(data=[], metadata={}, schema=None)

def test_interface_cannot_be_instantiated():
    with pytest.raises(TypeError):
        IDataCleaner()  # métodos abstratos não implementados

def test_dummy_implementation_respects_interface():
    cleaner = DummyDataCleaner()
    dummy_data = DummyRawData(data=[], metadata={}, schema=None)

    # fit() deve funcionar
    cleaner.fit(dummy_data)
    assert hasattr(cleaner, "fitted")

    # clean() só funciona depois do fit()
    cleaned = cleaner.clean(dummy_data)
    assert isinstance(cleaned, CleanedData)
