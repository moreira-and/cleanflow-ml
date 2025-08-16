from __future__ import annotations
from dataclasses import dataclass, field
from typing import Generic, Mapping, Optional, TypeVar, List, Dict, Any
from types import MappingProxyType
from uuid import uuid4
from datetime import datetime

from src.domain.entities.value_objects import (
    DatasetSchema,
    Provenance,
    ValidationStatus,
)

T = TypeVar("T")  # Tipo genérico para o payload de dados


@dataclass(frozen=True)
class BaseDataEntity(Generic[T]):
    """
    Core immutable domain artifact representing a dataset or intermediate data in ML pipelines.

    It carries data, its schema contract, provenance, validation status, identity/versioning
    and other optional ML-related metadata such as embeddings or feedback.
    """

    data: T = field(repr=False)
    schema: Optional[DatasetSchema] = field(default=None, repr=False)
    metadata: Mapping[str, Any] = field(default_factory=dict, repr=False)
    provenance: Optional[Provenance] = field(default=None, repr=False)
    validation_status: Optional[ValidationStatus] = field(default=None, repr=False)
    identity: str = field(default_factory=lambda: str(uuid4()))
    version: Optional[str] = field(default=None, repr=False)
    partition_info: Optional[str] = field(default=None, repr=False)
    lineage_id: Optional[str] = field(default=None, repr=False)
    embeddings: Optional[Any] = field(default=None, repr=False)
    feedback: Optional[Any] = field(default=None, repr=False)
    confidence: Optional[float] = field(default=None, repr=False)
    observation_time: Optional[datetime] = field(default=None, repr=False)

    def __post_init__(self):
        if self.data is None:
            raise ValueError("data cannot be None")
        object.__setattr__(self, "metadata", MappingProxyType(dict(self.metadata)))

    def is_compatible_with(self, other: BaseDataEntity) -> bool:
        if self.schema and other.schema:
            return (
                self.schema.columns == other.schema.columns
                and self.schema.targets == other.schema.targets
            )
        return False

    def with_updated_metadata(self, **extras) -> BaseDataEntity:
        new_meta = dict(self.metadata)
        new_meta.update(extras)
        return type(self)(
            data=self.data,
            schema=self.schema,
            metadata=new_meta,
            provenance=self.provenance,
            validation_status=self.validation_status,
            identity=self.identity,
            version=self.version,
            partition_info=self.partition_info,
            lineage_id=self.lineage_id,
            embeddings=self.embeddings,
            feedback=self.feedback,
            confidence=self.confidence,
            observation_time=self.observation_time,
        )

    def validate_against_schema(self) -> ValidationStatus:
        """
        Validate self.data against the attached schema and produce ValidationStatus.
        Must be called explicitly; does not mutate self (returns new status).
        """
        errors: List[str] = []
        warnings: List[str] = []
        details: Dict[str, Any] = {}

        if self.schema is None:
            errors.append("No schema provided.")
            return ValidationStatus(
                is_valid=False,
                errors=tuple(errors),
                warnings=tuple(warnings),
                details=details,
            )

        # Flatten rows depending on data shape
        # Expectation: self.data supports column access via dict-like or structured array semantics.
        # The implementation here is kept abstract; concrete adapters should normalize into a common inspection view.
        try:
            rows = self._extract_rows_for_validation()
        except Exception as e:
            errors.append(f"Failed to extract rows for validation: {e}")
            return ValidationStatus(
                is_valid=False,
                errors=tuple(errors),
                warnings=tuple(warnings),
                details=details,
            )

        # 1. Required columns existence
        missing_columns = [c for c in self.schema.columns if not self._column_exists(c)]
        if missing_columns:
            errors.append(f"Missing required feature columns: {missing_columns}")
            details["missing_columns"] = missing_columns

        # 2. Targets presence if supervised
        if self.schema.targets:
            missing_targets = [
                t for t in self.schema.targets if not self._column_exists(t)
            ]
            if missing_targets:
                errors.append(f"Missing required target columns: {missing_targets}")
                details["missing_targets"] = missing_targets

        # 3. Constraints
        if self.schema.constraints:
            not_null = self.schema.constraints.get("not_null", [])
            null_violations = []
            for col in not_null:
                if self._column_exists(col):
                    null_count = sum(1 for r in rows if r.get(col) is None)
                    if null_count > 0:
                        null_violations.append({col: null_count})
            if null_violations:
                errors.append(f"Not-null constraint violations: {null_violations}")
                details["not_null_violations"] = null_violations

            ranges = self.schema.constraints.get("range", {})
            range_violations = []
            for col, (low, high) in ranges.items():
                if self._column_exists(col):
                    out_of_bounds = []
                    for r in rows:
                        val = r.get(col)
                        if val is None:
                            continue
                        try:
                            if not (low <= val <= high):
                                out_of_bounds.append(val)
                        except TypeError:
                            range_violations.append(
                                {col: f"type mismatch for value {val}"}
                            )
                    if out_of_bounds:
                        range_violations.append({col: out_of_bounds[:5]})  # sample
            if range_violations:
                errors.append(f"Range constraint violations: {range_violations}")
                details["range_violations"] = range_violations

            allowed_values = self.schema.constraints.get("allowed_values", {})
            allowed_violations = []
            for col, allowed in allowed_values.items():
                if self._column_exists(col):
                    invalids = []
                    for r in rows:
                        val = r.get(col)
                        if val not in allowed and val is not None:
                            invalids.append(val)
                    if invalids:
                        allowed_violations.append({col: list(set(invalids))[:5]})
            if allowed_violations:
                warnings.append(f"Allowed-values deviations: {allowed_violations}")
                details["allowed_value_violations"] = allowed_violations

        # 4. Basic quality metrics (e.g., missing rate per column)
        missing_rate: Dict[str, float] = {}
        total_rows = len(rows) if rows else 0
        if total_rows > 0:
            for col in self.schema.columns + (self.schema.targets or []):
                if self._column_exists(col):
                    nulls = sum(1 for r in rows if r.get(col) is None)
                    missing_rate[col] = nulls / total_rows
            details["missing_rate"] = missing_rate
            high_missing = {
                col: rate for col, rate in missing_rate.items() if rate > 0.5
            }
            if high_missing:
                warnings.append(
                    f"High missing rate (>50%) in columns: {list(high_missing.keys())}"
                )

        is_valid = len(errors) == 0
        status = ValidationStatus(
            is_valid=is_valid,
            errors=tuple(errors),
            warnings=tuple(warnings),
            details=details if details else None,
        )
        return status

    # Internal helpers (could be overridden by subclasses or normalized by adapters)
    def _extract_rows_for_validation(self) -> List[Dict[str, Any]]:
        """
        Normalize self.data into list of row dicts for inspection.
        By default, attempts duck typing: structured array, list of dicts, object with to_dict(orient=...).
        """
        if isinstance(self.data, dict):
            # single record
            return [self.data]
        if hasattr(self.data, "to_dict"):
            try:
                # pandas-like
                return self.data.to_dict(orient="records")  # type: ignore
            except Exception:
                pass
        if hasattr(self.data, "__iter__") and not isinstance(self.data, (str, bytes)):
            # assume iterable of mappings or tuples with schema.columns order
            records = []
            for item in self.data:
                if isinstance(item, dict):
                    records.append(item)
                elif isinstance(item, (list, tuple)) and self.schema:
                    records.append(
                        {col: item[idx] for idx, col in enumerate(self.schema.columns)}
                    )
                else:
                    # fallback: store as single value
                    records.append({"value": item})
            return records
        raise ValueError("Unsupported data shape for validation extraction.")

    def _column_exists(self, column: str) -> bool:
        if self.schema and column in (self.schema.columns or []) + (
            self.schema.targets or []
        ):
            # presence in schema only; actual data presence is inferred via row inspection
            rows = []
            try:
                rows = self._extract_rows_for_validation()
            except Exception:
                return False
            return any(column in r for r in rows)
        return False

    def __repr__(self):
        base = ""
        if hasattr(self.data, "__len__"):
            try:
                length = len(self.data)
            except Exception:
                length = "?"
            base = f"rows={length}"
        else:
            base = f"type={type(self.data).__name__}"
        return f"{self.__class__.__name__}({base}, identity={self.identity}, version={self.version})"
