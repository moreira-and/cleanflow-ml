# 📦 Domain Layer Documentation

## Overview

The **domain layer** defines the business logic and modeling contracts of the ML pipeline. It captures high-level concepts such as data flow stages, transformations, schema constraints, and learning strategies. This layer is designed to be:

* **Framework-agnostic** – no dependency on external libraries.
* **Fully testable** – all logic can be validated using pure unit tests.
* **Immutable and type-safe** – entities are declared as `@dataclass(frozen=True)` with explicit types.
* **Stable and composable** – changes to infrastructure or orchestration do not affect domain logic.

The domain is the **center of gravity** of the system: everything else (infra, application, orchestration) revolves around the rules defined here.

---

## Core Abstractions

### Entities

Entities in this domain model represent immutable **data containers** used to carry data between stages:

| Entity            | Description                                            |
| ----------------- | ------------------------------------------------------ |
| `RawData`         | Input data as received from upstream systems.          |
| `CleanedData`     | Sanitized version of `RawData`.                        |
| `SelectedData`    | Feature subset or filtered version of `CleanedData`.   |
| `ModelInputData`  | Final model-ready representation.                      |
| `ModelOutputData` | Output from ML model, usually unstructured or encoded. |
| `PredictedData`   | Post-processed domain-level predictions.               |

All entities inherit from:

```python
BaseDataEntity[T]
```

Which encapsulates:

* `data: T` – a numpy array, pandas DataFrame, or any structured object.
* `metadata: Mapping[str, Any]` – contextual, frozen key-value store.
* `schema: Optional[DatasetSchema]` – column definitions, targets, description.

This makes the system generic and ready for integration with traditional ML and LLM pipelines.

---

### Value Objects

* **`DatasetSchema`**: Describes expected structure of datasets (columns, targets, etc.).
* **`ProblemType`**: Enum that identifies the nature of the task (e.g., regression, classification).

---

### Domain Interfaces

Each stage of the ML flow is abstracted as a domain interface:

| Stage     | Interface       | Responsibilities                                  |
| --------- | --------------- | ------------------------------------------------- |
| Cleaning  | `IDataCleaner`  | Prepares and applies rules to sanitize raw input. |
| Selection | `IDataSelector` | Extracts relevant features or rows.               |
| Adapting  | `IDataAdapter`  | Transforms data to/from model-compatible formats. |
| Modeling  | `IModel`        | Trains and infers predictions using ML logic.     |

All interfaces follow a **Prepare → Apply** pattern:

#### Example: IDataCleaner

```python
def prepare(data: RawData) -> CleaningSummary
def clean(data: RawData, config: CleaningConfig) -> CleanedData
```

#### Example: IModel

```python
def prepare_training(problem_type, data) -> TrainingSummary
def train(problem_type, data, config) -> None

def prepare_prediction(data) -> PredictionSummary
def predict(data, config) -> ModelOutputData
```

This pattern:

* Avoids hidden mutable state.
* Makes orchestration stateless and modular.
* Improves auditability, versioning, and reproducibility.

---

## Stage Contracts

All `prepare()` methods return **summary objects**, which include:

* `config`: the configuration to be passed to the corresponding `apply()` method.
* `observations`: metadata or diagnostics to help audit, explain, or validate the decision.

| Stage           | Config Class           | Summary Class           |
| --------------- | ---------------------- | ----------------------- |
| Cleaner         | `CleaningConfig`       | `CleaningSummary`       |
| Selector        | `SelectionConfig`      | `SelectionSummary`      |
| Adapter (fwd)   | `TransformationConfig` | `TransformationSummary` |
| Adapter (inv)   | `InverseConfig`        | `InverseSummary`        |
| Model (train)   | `TrainingConfig`       | `TrainingSummary`       |
| Model (predict) | `PredictionConfig`     | `PredictionSummary`     |

These contracts enable strong test coverage and pluggable implementations.

---

## Architectural Principles

This domain layer is built on:

### ✅ Clean Architecture

* **Domain logic is isolated** from frameworks and infrastructure.
* **Only the domain knows the meaning of the data**; application and infra only orchestrate.
* Domain interfaces are implemented externally and injected via dependency inversion.

### ✅ DDD (Domain-Driven Design)

* Interfaces describe *ubiquitous language*: “cleaner”, “selector”, “adapter”, “model”.
* Value objects and entities are immutable and self-validating.
* Rules about the data live in the domain; orchestration lives in the application layer.

---

## Example Usage

```python
# In the application layer

summary = selector.prepare(cleaned_data)
selected_data = selector.select(cleaned_data, summary.config)

summary = adapter.prepare_transform(selected_data)
model_input = adapter.transform(selected_data, summary.config)

prediction_summary = model.prepare_prediction(model_input)
model_output = model.predict(model_input, prediction_summary.config)
```

---

## Test Contracts

For each interface, **domain test contracts** are defined to enforce expected behaviors:

* `test_data_cleaner_contract.py`
* `test_data_selector_contract.py`
* `test_data_adapter_contract.py`
* `test_model_contract.py`

These contracts ensure all implementations:

* Are deterministic
* Produce consistent config/output pairs
* Fail gracefully on invalid input
* Maintain traceability via metadata

---

## Extensibility

This domain layer is designed to support:

* ML pipelines with scikit-learn, XGBoost, LightGBM, TensorFlow, or PyTorch.
* Dynamic orchestration of stages via factories or dependency injection.
* Compatibility with batch, streaming, or hybrid data workflows.
* Future integration with large language models (LLMs) using the same data abstractions.