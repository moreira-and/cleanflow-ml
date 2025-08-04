from src.domain.entities.data.cleaned_data import CleanedData
from src.domain.entities.data.selected_data import SelectedData
from abc import ABC, abstractmethod

class IDataSelector(ABC):
    """
    Interface for implementing data selection strategies within the domain layer.
    
    This interface defines a contract for components responsible for selecting relevant
    features or rows from pre-processed (cleaned) data. Implementations may include
    feature selection algorithms, dimensionality reduction, or rule-based filtering.

    Methods:
        fit(data: CleanedData) -> None:
            Fit the selector to the given cleaned data. 
            Used to learn parameters or compute statistics required for selection.

        select(data: CleanedData) -> SelectedData:
            Apply the selection logic to the cleaned data and return the resulting subset.
    """

    @abstractmethod
    def fit(self, data: CleanedData) -> None:
        """
        Fit the selector to the provided cleaned data.

        Args:
            data (CleanedData): The cleaned dataset to fit the selector on.
        """
        pass

    @abstractmethod
    def select(self, data: CleanedData) -> SelectedData:
        """
        Select relevant features or records from the cleaned data.

        Args:
            data (CleanedData): The cleaned dataset to apply the selection to.

        Returns:
            SelectedData: The result of applying the selection logic.
        """
        pass
