from abc import ABC, abstractmethod
from typing import List, Dict, TypeVar

# Define a type variable that can be any type
T = TypeVar('T')

class DataSource(ABC):
    """Abstract Base Class for getting and processing data"""
    @abstractmethod
    def fetch_data(self) -> List[T]:
        """Fetch the raw data from an external source."""
        pass

    @abstractmethod
    def process_data(self, raw_data: List[T]) -> List[T]:
        """Process raw data and extract relevant information."""
        pass

    def get_data(self) -> List[T]:
        """Fetch and process data, then return the processed data."""
        raw_data = self.fetch_data()
        processed_data = self.process_data(raw_data)
        return processed_data