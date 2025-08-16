import pytest
from abc import ABC, abstractmethod
from src.domain.entities.stages.raw_data import RawData
from src.domain.entities.stages.cleaned_data import CleanedData
from src.domain.interfaces.strategies.i_data_cleaner import (
    IDataCleaner,
    CleaningConfig,
    CleaningSummary,
)


class DataCleanerContract(ABC):
    """
    Contract tests for any IDataCleaner implementation.
    Concrete test modules must provide:
      - cleaner_factory: callable returning a fresh IDataCleaner
      - sample_raw_data: RawData containing known quality issues
      - valid_raw_data: RawData that is already clean
      - schema_preserving_checker: callable(cleaned: CleanedData, original: RawData) -> bool
    """

    @pytest.fixture
    @abstractmethod
    def cleaner_factory(self) -> callable: ...

    @pytest.fixture
    @abstractmethod
    def sample_raw_data(self) -> RawData: ...

    @pytest.fixture
    @abstractmethod
    def valid_raw_data(self) -> RawData: ...

    @pytest.fixture
    @abstractmethod
    def schema_preserving_checker(self) -> callable: ...

    def test_prepare_returns_summary_with_config_and_issues(
        self, cleaner_factory, sample_raw_data
    ):
        cleaner: IDataCleaner = cleaner_factory()
        summary: CleaningSummary = cleaner.prepare(sample_raw_data)
        assert isinstance(summary, CleaningSummary)
        assert isinstance(summary.config, CleaningConfig)
        assert summary.issues, "Expected issues detected in sample_raw_data"

    def test_clean_applies_based_on_config(
        self, cleaner_factory, sample_raw_data, schema_preserving_checker
    ):
        cleaner: IDataCleaner = cleaner_factory()
        summary: CleaningSummary = cleaner.prepare(sample_raw_data)
        cleaned: CleanedData = cleaner.clean(sample_raw_data, summary.config)
        assert isinstance(cleaned, CleanedData)
        assert schema_preserving_checker(cleaned, sample_raw_data)

    def test_idempotency_of_clean(self, cleaner_factory, sample_raw_data):
        cleaner: IDataCleaner = cleaner_factory()
        summary: CleaningSummary = cleaner.prepare(sample_raw_data)
        first: CleanedData = cleaner.clean(sample_raw_data, summary.config)
        second: CleanedData = cleaner.clean(first, summary.config)
        assert first == second, (
            "Cleaner should be idempotent when reapplied with same config"
        )

    def test_no_op_on_valid_data(
        self, cleaner_factory, valid_raw_data, schema_preserving_checker
    ):
        cleaner: IDataCleaner = cleaner_factory()
        summary: CleaningSummary = cleaner.prepare(valid_raw_data)
        cleaned: CleanedData = cleaner.clean(valid_raw_data, summary.config)
        assert schema_preserving_checker(cleaned, valid_raw_data)
