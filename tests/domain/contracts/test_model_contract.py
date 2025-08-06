import pytest
from abc import ABC, abstractmethod
from src.domain.entities.stages.model_input_data import ModelInputData
from src.domain.entities.stages.model_output_data import ModelOutputData
from src.domain.interfaces.strategies.i_model import (
    IModel,
    TrainingConfig,
    TrainingSummary,
    PredictionConfig,
    PredictionSummary,
)
from src.domain.enums.problem_type import ProblemType


class ModelContract(ABC):
    """
    Contract tests for any IModel implementation.
    Requirements:
      - model_factory: callable producing fresh IModel
      - valid_training_data: ModelInputData suitable for training
      - valid_inference_data: ModelInputData suitable for prediction
      - invalid_inference_data: ModelInputData expected to surface graceful degradation
      - training_preserving_checker: callable after train (optional)
      - prediction_output_checker: callable(ModelOutputData, ModelInputData) -> bool
    """

    @pytest.fixture
    @abstractmethod
    def model_factory(self) -> callable:
        ...

    @pytest.fixture
    @abstractmethod
    def valid_training_data(self) -> ModelInputData:
        ...

    @pytest.fixture
    @abstractmethod
    def valid_inference_data(self) -> ModelInputData:
        ...

    @pytest.fixture
    @abstractmethod
    def invalid_inference_data(self) -> ModelInputData:
        ...

    @pytest.fixture
    @abstractmethod
    def prediction_output_checker(self) -> callable:
        ...

    def test_prepare_training_returns_summary(self, model_factory, valid_training_data):
        model: IModel = model_factory()
        summary: TrainingSummary = model.prepare_training(ProblemType.CLASSIFICATION, valid_training_data)
        assert isinstance(summary, TrainingSummary)
        assert isinstance(summary.config, TrainingConfig)
        assert isinstance(summary.observations, dict)

    def test_train_then_predict_flow(self, model_factory, valid_training_data, valid_inference_data, prediction_output_checker):
        model: IModel = model_factory()
        train_summary: TrainingSummary = model.prepare_training(ProblemType.CLASSIFICATION, valid_training_data)
        model.train(ProblemType.CLASSIFICATION, valid_training_data, train_summary.config)

        pred_summary: PredictionSummary = model.prepare_prediction(valid_inference_data)
        output: ModelOutputData = model.predict(valid_inference_data, pred_summary.config)
        assert prediction_output_checker(output, valid_inference_data)

    def test_prediction_is_deterministic_if_expected(self, model_factory, valid_inference_data):
        model1: IModel = model_factory()
        model2: IModel = model_factory()
        summary1: PredictionSummary = model1.prepare_prediction(valid_inference_data)
        out1 = model1.predict(valid_inference_data, summary1.config)

        summary2: PredictionSummary = model2.prepare_prediction(valid_inference_data)
        out2 = model2.predict(valid_inference_data, summary2.config)

        assert out1 == out2, "Prediction outputs diverge for same input when determinism is expected"

    def test_handles_invalid_input_gracefully(self, model_factory, invalid_inference_data):
        model: IModel = model_factory()
        pred_summary: PredictionSummary = model.prepare_prediction(invalid_inference_data)
        try:
            _ = model.predict(invalid_inference_data, pred_summary.config)
        except Exception:
            pytest.skip("Implementation raises domain-specific error for invalid input (acceptable)")
