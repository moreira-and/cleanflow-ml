from dataclasses import FrozenInstanceError
from src.domain.entities.data.cleaned_data import CleanedData  # ajuste o path real do seu projeto
import pytest
import pandas as pd

def test_cleaned_data_instantiation_with_dataframe():
    df = pd.DataFrame({"col": [1, 2, 3]})
    entity = CleanedData(data=df)
    
    assert isinstance(entity, CleanedData)
    assert (entity.data == df).all().all()

def test_cleaned_data_instantiation_with_dict():
    d = {"a": 1, "b": 2}
    entity = CleanedData(data=d)
    
    assert entity.data == d

def test_cleaned_data_is_immutable():
    entity = CleanedData(data={"test": 123})
    
    with pytest.raises(FrozenInstanceError):
        entity.data = {"new": 456}

def test_cleaned_data_equality():
    d1 = {"x": 1}
    d2 = {"x": 1}
    
    e1 = CleanedData(data=d1)
    e2 = CleanedData(data=d2)
    
    assert e1 == e2
    assert hash(e1) == hash(e2)
