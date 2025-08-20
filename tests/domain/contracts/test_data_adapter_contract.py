import pytest
from abc import ABC, abstractmethod
from src.domain.entities.stages.selected_data import SelectedData
from src.domain.entities.stages.model_input_data import ModelInputData
from src.domain.entities.stages.model_output_data import ModelOutputData
from src.domain.entities.stages.predicted_data import PredictedData
from domain.interfaces.strategies.i_model_adapter import (
    IModelAdapter,
    TransformationConfig,
    TransformationSummary,
    InverseConfig,
    InverseSummary,
)


class DataAdapterContract(ABC):
    """
    Contract tests for any IDataAdapter implementation.
    Requirements:
      - adapter_factory: callable returning fresh IDataAdapter
      - sample_selected_data: SelectedData for forward transform
      - valid_selected_data: SelectedData that should round-trip cleanly
      - model_output_data: ModelOutputData to test inverse path
      - forward_preserving_checker: callable(ModelInputData, SelectedData) -> bool
      - inverse_preserving_checker: callable(PredictedData, ModelOutputData) -> bool
    """

    @pytest.fixture
    @abstractmethod
    def adapter_factory(self) -> callable: ...

    @pytest.fixture
    @abstractmethod
    def sample_selected_data(self) -> SelectedData: ...

    @pytest.fixture
    @abstractmethod
    def valid_selected_data(self) -> SelectedData: ...

    @pytest.fixture
    @abstractmethod
    def model_output_data(self) -> ModelOutputData: ...

    @pytest.fixture
    @abstractmethod
    def forward_preserving_checker(self) -> callable: ...

    @pytest.fixture
    @abstractmethod
    def inverse_preserving_checker(self) -> callable: ...

    def test_prepare_transform_returns_summary(
        self, adapter_factory, sample_selected_data
    ):
        adapter: IModelAdapter = adapter_factory()
        summary: TransformationSummary = adapter.prepare_transform(sample_selected_data)
        assert isinstance(summary, TransformationSummary)
        assert isinstance(summary.config, TransformationConfig)
        assert isinstance(summary.observations, dict)

    def test_transform_and_preserve_schema(
        self, adapter_factory, valid_selected_data, forward_preserving_checker
    ):
        adapter: IModelAdapter = adapter_factory()
        summary: TransformationSummary = adapter.prepare_transform(valid_selected_data)
        model_input: ModelInputData = adapter.transform(
            valid_selected_data, summary.config
        )
        assert forward_preserving_checker(model_input, valid_selected_data)

    def test_prepare_inverse_returns_summary(self, adapter_factory, model_output_data):
        adapter: IModelAdapter = adapter_factory()
        summary: InverseSummary = adapter.prepare_inverse(model_output_data)
        assert isinstance(summary, InverseSummary)
        assert isinstance(summary.config, InverseConfig)
        assert isinstance(summary.observations, dict)

    def test_inverse_transform_and_preserve(
        self, adapter_factory, model_output_data, inverse_preserving_checker
    ):
        adapter: IModelAdapter = adapter_factory()
        inv_summary: InverseSummary = adapter.prepare_inverse(model_output_data)
        predicted: PredictedData = adapter.inverse_transform(
            model_output_data, inv_summary.config
        )
        assert inverse_preserving_checker(predicted, model_output_data)
