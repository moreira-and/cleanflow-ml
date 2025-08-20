import pytest
from abc import ABC, abstractmethod
from src.domain.entities.stages.cleaned_data import CleanedData
from src.domain.entities.stages.selected_data import SelectedData
from domain.interfaces.strategies.i_feature_selector import (
    IFeatureSelector,
    SelectionConfig,
    SelectionSummary,
)


class DataSelectorContract(ABC):
    """
    Contract tests for any IDataSelector implementation.
    Requirements:
      - selector_factory: callable returning fresh IDataSelector
      - sample_cleaned_data: CleanedData with irrelevant/noisy features
      - valid_cleaned_data: CleanedData already appropriately selected
      - selection_preserving_checker: callable(selected: SelectedData, original: CleanedData) -> bool
    """

    @pytest.fixture
    @abstractmethod
    def selector_factory(self) -> callable: ...

    @pytest.fixture
    @abstractmethod
    def sample_cleaned_data(self) -> CleanedData: ...

    @pytest.fixture
    @abstractmethod
    def valid_cleaned_data(self) -> CleanedData: ...

    @pytest.fixture
    @abstractmethod
    def selection_preserving_checker(self) -> callable: ...

    def test_prepare_returns_summary_with_config_and_observations(
        self, selector_factory, sample_cleaned_data
    ):
        selector: IFeatureSelector = selector_factory()
        summary: SelectionSummary = selector.prepare(sample_cleaned_data)
        assert isinstance(summary, SelectionSummary)
        assert isinstance(summary.config, SelectionConfig)
        assert isinstance(summary.observations, dict)

    def test_select_applies_based_on_config(
        self, selector_factory, sample_cleaned_data, selection_preserving_checker
    ):
        selector: IFeatureSelector = selector_factory()
        summary: SelectionSummary = selector.prepare(sample_cleaned_data)
        selected: SelectedData = selector.select(sample_cleaned_data, summary.config)
        assert isinstance(selected, SelectedData)
        assert selection_preserving_checker(selected, sample_cleaned_data)

    def test_idempotent_selection(self, selector_factory, valid_cleaned_data):
        selector: IFeatureSelector = selector_factory()
        summary: SelectionSummary = selector.prepare(valid_cleaned_data)
        first: SelectedData = selector.select(valid_cleaned_data, summary.config)
        second: SelectedData = selector.select(first, summary.config)
        assert first == second, (
            "Selection should be idempotent on already selected data"
        )

    def test_no_destructive_on_valid(
        self, selector_factory, valid_cleaned_data, selection_preserving_checker
    ):
        selector: IFeatureSelector = selector_factory()
        summary: SelectionSummary = selector.prepare(valid_cleaned_data)
        selected: SelectedData = selector.select(valid_cleaned_data, summary.config)
        assert selection_preserving_checker(selected, valid_cleaned_data)
