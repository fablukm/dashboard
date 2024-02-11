from abc import ABC, abstractmethod
from typing import List, Dict, TypeVar
from .weather import WeatherDataSource

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


def get_dashboard_data():
    # weather
    weather_data_source = WeatherDataSource()
    weather_data = weather_data_source.process_data()

    dashbard_api_response = {
        "time_weather": weather_data,
        "events": [
            {"name": "Meeting with team", "time": "11:00 AM"},
            {"name": "Doctor's Appointment", "time": "3:00 PM"}
        ],
        "unread_emails": 5,
        "public_transport": [
            {"station": "Station A", "connection": "Bus 10 - 10:15 AM"},
            {"station": "Station B", "connection": "Train 5 - 10:30 AM"},
            {"station": "Station C", "connection": "Tram 2 - 10:45 AM"}
        ]
    }
    return dashbard_api_response