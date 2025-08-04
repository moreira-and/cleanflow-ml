from src.domain.entities.data.raw_data import RawData
from src.domain.entities.data.cleaned_data import CleanedData
from abc import ABC, abstractmethod

class IDataCleaner(ABC):
    """
    Interface for defining data cleaning strategies in a model-agnostic and domain-driven context.

    It isolates the logic for transforming raw, unstructured, or inconsistent input data into a 
    clean and structured form ready for analysis or modeling. By abstracting this process, the 
    interface enables the infrastructure layer to implement diverse cleaning techniques while 
    ensuring orchestration consistency in the application layer.

    Typical responsibilities include:
    - Handling missing values, outliers, and inconsistent formats.
    - Applying domain-specific rules to validate or correct data.
    - Generating metadata to guide or document the cleaning process.

    Methods:
        fit(data: RawData) -> None:
            Inspects the raw dataset to extract metadata, rules, or thresholds
            that inform the subsequent cleaning logic. This step may compute statistics,
            detect patterns, or flag anomalies.

        clean(data: RawData) -> CleanedData:
            Applies the transformation logic—either predefined or derived during `fit`—
            to produce a cleaned, structured, and reliable version of the dataset.
    """

    @abstractmethod
    def fit(self, data: RawData) -> None:
        """
        Analyze raw data to extract metadata or define dynamic cleaning rules.

        Args:
            data (RawData): The original, unprocessed dataset that may contain
                            inconsistencies, missing values, or noise.
        """
        pass

    @abstractmethod
    def clean(self, data: RawData) -> CleanedData:
        """
        Execute the cleaning process based on static rules or parameters learned in `fit`.

        Args:
            data (RawData): The dataset to be cleaned.

        Returns:
            CleanedData: The resulting dataset after applying cleaning logic,
                         now structured and ready for downstream use.
        """
        pass
