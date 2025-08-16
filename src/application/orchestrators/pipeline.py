from typing import Any, Callable


class Pipeline:
    def __init__(self):
        self._stages: list[Callable[[Any], Any]] = []

    def add_stage(self, stage: Callable[[Any], Any]) -> "Pipeline":
        self._stages.append(stage)
        return self

    def run(self, data: Any) -> Any:
        result = data
        for stage in self._stages:
            result = stage(result)
        return result
