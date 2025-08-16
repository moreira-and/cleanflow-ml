from dataclasses import dataclass
from datetime import datetime
from typing import Tuple


@dataclass(frozen=True)
class Provenance:
    """
    Provenance information for a data artifact.

    Attributes:
        source: Logical origin (e.g., filename, stream name, upstream step).
        extraction_time: When the raw capture happened.
        transforms: Ordered tuple of transformation identifiers already applied.
    """

    source: str
    extraction_time: datetime
    transforms: Tuple[str, ...] = ()

    def __post_init__(self):
        if not isinstance(self.source, str):
            raise TypeError("source must be a string")
        if not isinstance(self.extraction_time, datetime):
            raise TypeError("extraction_time must be a datetime object")
        if self.extraction_time.tzinfo is None:
            # assume UTC se não tiver tz
            self.extraction_time = self.extraction_time.replace(tzinfo=timezone.utc)
