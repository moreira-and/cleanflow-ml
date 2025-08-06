import pytest
from datetime import datetime
from src.domain.entities.base_data_entity import (
    BaseDataEntity,
    DatasetSchema,
    Provenance,
)

# Helper to build simple mock data
def make_entity(data, schema=None):
    return BaseDataEntity(
        data=data,
        schema=schema,
        provenance=Provenance(source="unit_test", extraction_time=datetime.now())
    )

def test_missing_schema_returns_invalid_status():
    entity = make_entity([{"a": 1, "b": 2}], schema=None)
    status = entity.validate_against_schema()
    assert status.is_valid is False
    assert "No schema provided." in status.errors

def test_missing_feature_column_is_detected():
    schema = DatasetSchema(columns=["a", "b", "c"])
    entity = make_entity([{"a": 1, "b": 2}], schema=schema)
    status = entity.validate_against_schema()
    assert status.is_valid is False
    assert any("Missing required feature columns" in err for err in status.errors)
    assert "c" in status.details["missing_columns"]

def test_missing_target_column_is_detected():
    schema = DatasetSchema(columns=["a", "b"], targets=["y"])
    entity = make_entity([{"a": 1, "b": 2}], schema=schema)
    status = entity.validate_against_schema()
    assert status.is_valid is False
    assert "Missing required target columns" in status.errors[0]
    assert "y" in status.details["missing_targets"]

def test_not_null_violation_detected():
    schema = DatasetSchema(
        columns=["a", "b"],
        constraints={"not_null": ["a", "b"]}
    )
    data = [{"a": 1, "b": 2}, {"a": None, "b": 3}, {"a": 2, "b": None}]
    entity = make_entity(data, schema=schema)
    status = entity.validate_against_schema()
    assert status.is_valid is False
    assert any("Not-null constraint violations" in err for err in status.errors)
    assert "a" in str(status.details["not_null_violations"])
    assert "b" in str(status.details["not_null_violations"])

def test_range_constraint_detected():
    schema = DatasetSchema(
        columns=["score"],
        constraints={"range": {"score": (0, 10)}}
    )
    data = [{"score": 5}, {"score": 12}, {"score": -1}]
    entity = make_entity(data, schema=schema)
    status = entity.validate_against_schema()
    assert status.is_valid is False
    assert "Range constraint violations" in status.errors[0]
    assert "score" in str(status.details["range_violations"])

def test_allowed_values_warning_detected():
    schema = DatasetSchema(
        columns=["category"],
        constraints={"allowed_values": {"category": ["A", "B", "C"]}}
    )
    data = [{"category": "A"}, {"category": "X"}, {"category": "Y"}]
    entity = make_entity(data, schema=schema)
    status = entity.validate_against_schema()
    assert status.is_valid is True  # only warning
    assert "Allowed-values deviations" in status.warnings[0]
    assert "X" in str(status.details["allowed_value_violations"])
    assert "Y" in str(status.details["allowed_value_violations"])

def test_missing_rate_metrics_calculated():
    schema = DatasetSchema(columns=["a", "b"])
    data = [{"a": 1, "b": None}, {"a": None, "b": None}, {"a": 1, "b": 1}]
    entity = make_entity(data, schema=schema)
    status = entity.validate_against_schema()
    assert status.is_valid is True
    assert "missing_rate" in status.details
    assert status.details["missing_rate"]["a"] == pytest.approx(1/3)
    assert status.details["missing_rate"]["b"] == pytest.approx(2/3)
    assert "High missing rate" in status.warnings[0]
