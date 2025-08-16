# src/domain/contracts/data_validator.py
from abc import ABC, abstractmethod
from src.domain.entities.base import BaseDataEntity
from src.domain.entities.value_objects import ValidationStatus


class IDataValidator(ABC):
    """
    Contract for validating domain data entities.

    This interface defines the expected behavior of any validator that
    inspects a domain-level data entity and returns a validation status.
    The goal is to standardize validation logic across implementations
    without tying the domain to specific libraries or frameworks.

    Responsibilities:
    - Check data integrity (e.g., missing values, type mismatches).
    - Enforce schema compliance if defined.
    - Return structured feedback via ValidationStatus.

    Typical implementations:
    - Pandas-based validator for tabular datasets.
    - JSON schema validator for structured payloads.
    - Custom rule-based validator for business constraints.
    """

    @abstractmethod
    def validate(self, entity: BaseDataEntity) -> ValidationStatus:
        """
        Validate the given domain entity.

        Args:
            entity (BaseDataEntity): Domain-level data entity containing
                                     data and optional schema metadata.

        Returns:
            ValidationStatus: Structured result indicating whether the
                              entity passed validation, including any
                              errors or warnings.
        """
        pass
