import pytest
from types import MappingProxyType
from src.domain.entities.base import BaseDataEntity, DatasetSchema

class DummySchema(DatasetSchema):
    pass  # implemente o necessário ou use um mock

def test_base_data_entity_creation_and_repr():
    data = [1, 2, 3]
    metadata = {"source": "unit_test", "version": 1}
    schema = DummySchema()  # use um mock/objeto válido

    entity = BaseDataEntity(data=data, metadata=metadata, schema=schema)

    # data correto
    assert entity.data == data

    # metadata imutável (não pode alterar)
    with pytest.raises(TypeError):
        entity.metadata["new_key"] = "fail"

    # schema correto
    assert entity.schema == schema

    # __repr__ inclui "rows"
    r = repr(entity)
    assert "rows=3" in r

def test_base_data_entity_data_none_raises():
    with pytest.raises(ValueError):
        BaseDataEntity(data=None)

def test_repr_without_len():
    class CustomObj:
        pass

    obj = CustomObj()
    entity = BaseDataEntity(data=obj)
    r = repr(entity)
    assert f"type={obj.__class__.__name__}" in r
