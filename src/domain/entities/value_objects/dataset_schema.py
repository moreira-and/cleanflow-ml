from dataclasses import dataclass
from typing import Optional, Dict, Any


@dataclass(frozen=True)
class DatasetSchema:
    """
    Schema definition for a dataset in the domain.

    Attributes:
        columns: List of feature column names.
        targets: Optional list of target/label column names.
        feature_types: Optional map of column -> semantic type (e.g., "numeric", "categorical", "datetime").
        constraints: Optional constraints, e.g.:
            {
                "not_null": ["col_a", "col_b"],
                "range": {"col_c": (0, 1)},
                "allowed_values": {"col_d": ["A", "B", "C"]}
            }
        description: Human-readable description.
        version: Optional version string for the schema itself.
    """

    columns: list[str]
    targets: Optional[list[str]] = None
    feature_types: Optional[Dict[str, str]] = None
    constraints: Optional[Dict[str, Any]] = None
    description: Optional[str] = None
    version: Optional[str] = None

    def __post_init__(self):
        if not self.columns:
            raise ValueError("columns must not be empty")
        if self.targets is not None and not isinstance(self.targets, list):
            raise TypeError("targets must be a list or None")
        if self.description is not None and not isinstance(self.description, str):
            raise TypeError("description must be a string or None")
