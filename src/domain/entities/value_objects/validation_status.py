from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class ValidationStatus:
    """
    Result of validating a BaseDataEntity against its expected schema and quality rules.

    Attributes:
        is_valid: True if no blocking issues were found.
        errors: Blocking issues (schema mismatch, missing required targets, constraint violations).
        warnings: Non-blocking but noteworthy deviations (e.g., high missing rate).
        details: Optional structured data for downstream introspection.
    """

    is_valid: bool
    errors: tuple[str, ...] = ()
    warnings: tuple[str, ...] = ()
    details: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if not isinstance(self.is_valid, bool):
            raise TypeError("is_valid must be a boolean")
        if not isinstance(self.errors, tuple):
            raise TypeError("errors must be a tuple of strings")
        if not isinstance(self.warnings, tuple):
            raise TypeError("warnings must be a tuple of strings")
        if not isinstance(self.details, dict):
            raise TypeError("details must be a dictionary")

        # Ensure all errors and warnings are strings
        for error in self.errors:
            if not isinstance(error, str):
                raise TypeError("All errors must be strings")
        for warning in self.warnings:
            if not isinstance(warning, str):
                raise TypeError("All warnings must be strings")
