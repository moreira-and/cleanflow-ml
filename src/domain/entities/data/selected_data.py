from typing import TypeVar, Generic
from dataclasses import dataclass

T = TypeVar("T")

@dataclass(frozen=True)
class SelectedData(Generic[T]):
    data: T

    def __post_init__(self):
        if self.data is None:
            raise ValueError("Data cannot be None")