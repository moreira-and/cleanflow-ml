from dataclasses import dataclass
from typing import Generic, TypeVar

from domain.entities.base_data_entity import BaseDataEntity

T = TypeVar("T")

@dataclass(frozen=True)
class ModelOutputData(BaseDataEntity[T], Generic[T]):
    """
    Represents data predicted entity for a model in the semantic pipeline layer.

    This class serves as a domain entity encapsulating data that has 
    undergone cleaning or preprocessing steps. It is generic over the 
    data type T to support flexibility in the kind of data it holds 
    (e.g., pandas DataFrame, numpy array, custom data structures).

    Being a frozen dataclass, instances are immutable, ensuring data 
    consistency throughout the pipeline stages.

    Inherits from BaseDataEntity to leverage common data and metadata 
    handling functionality.
    """
    pass