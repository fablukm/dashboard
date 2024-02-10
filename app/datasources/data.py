from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Dict

@dataclass
class ProcessedData:
    timestamp: str
    raw_data: List[Dict]
    processed_data: List[Dict]


class DataSource(ABC):
    """Abstract Base Class for getting and processing data"""
    @abstractmethod
    def fetch_data(self) -> List[Dict]:
        """Fetch the raw data from an external source."""
        pass

    @abstractmethod
    def process_data(self, raw_data: List[Dict]) -> List[Dict]:
        """Process raw data and extract relevant information."""
        pass

    def get_data(self) -> List[Dict]:
        """Fetch and process data, then return the processed data."""
        raw_data = self.fetch_data()
        processed_data = self.process_data(raw_data)
        return processed_data


def get_dashboard_data():
    return {
        "time_weather": {
            "location": "Your City",
            "time": "10:00 AM",
            "weather": "Sunny, 25°C",
            "weatherId": 801,
            "additional_locations": [
                {"location": "New York", "time": "9:00 AM", "weather": "Cloudy", "weatherId": 801},
                {"location": "London", "time": "2:00 PM", "weather": "Rainy", "weatherId": 300},
            ]
        },
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