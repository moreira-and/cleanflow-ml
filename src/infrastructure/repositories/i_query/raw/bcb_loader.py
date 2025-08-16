from domain.interfaces.repositories import IQuery
from typing import Any, Mapping


class BcbLoader(IQuery):
    def get_by_id(self, ids: list[str] = None) -> Mapping[str, Any]:
        return {i: f"BCB_data({i})" for i in ids}

    def list_all(self) -> list[Any]:
        return ["BCB_data1", "BCB_data2"]
