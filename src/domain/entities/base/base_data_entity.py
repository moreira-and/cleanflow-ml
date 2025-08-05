from .dataset_schema import DatasetSchema
from dataclasses import dataclass, field
from typing import Any, Generic, TypeVar, Mapping, Optional

T = TypeVar("T")

@dataclass(frozen=True)
class BaseDataEntity(Generic[T]):
    """
    Immutable base domain entity encapsulating data with its schema and metadata.

    This class couples the data payload with a formal schema describing its structure,
    enabling domain-level understanding and validation of data contents.

    It enforces immutability and minimal validation, specifically disallowing None data.

    Attributes:
        schema (DatasetSchema): Formal schema defining columns, targets, and related metadata.
        data (T): The core data content (e.g., DataFrame, numpy array, etc.).
        metadata (Mapping[str, Any]): Immutable contextual metadata, such as provenance or tags.

    Notes:
        - This entity does not defensively copy `data`; immutability must be guaranteed upstream.
        - Metadata is stored as a read-only mapping to prevent unintended modifications.

    Methods:
        __repr__: Provides a concise string including data size or type information.
    """

    data: T = field(repr=False)
    metadata: Mapping[str, Any] = field(default_factory=dict, repr=False)
    schema: Optional[DatasetSchema] = field(default=None, repr=False)


    def __post_init__(self):
        if self.data is None:
            raise ValueError("data cannot be None or null")

    def __repr__(self):
        if hasattr(self.data, "__len__"):
            return f"{self.__class__.__name__}(rows={len(self.data)})"
        return f"{self.__class__.__name__}(type={type(self.data).__name__})"
