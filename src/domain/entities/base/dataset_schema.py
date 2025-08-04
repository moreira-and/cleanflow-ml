from dataclasses import dataclass, field
from typing import List, Optional

@dataclass(frozen=True)
class DatasetSchema:
    """
    Represents the schema of a dataset in the domain layer.

    Attributes:
        columns (List[str]): List of feature column names.
        targets (Optional[List[str]]): List of target/label column names for supervised tasks.
        description (Optional[str]): Optional human-readable description of the dataset schema.
    """

    columns: List[str] = field(default_factory=list)
    targets: Optional[List[str]] = field(default=None)
    description: Optional[str] = field(default=None)
