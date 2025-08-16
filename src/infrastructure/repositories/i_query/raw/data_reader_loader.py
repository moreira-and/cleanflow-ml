from domain.interfaces.repositories import IQuery
from typing import Any, Mapping


class DataReaderLoader(IQuery):
    def get_by_id(self, ids: list[str] = None) -> Mapping[str, Any]:
        return {i: f"DR_data({i})" for i in ids}

    def list_all(self) -> list[Any]:
        return ["DR_data1", "DR_data2"]
