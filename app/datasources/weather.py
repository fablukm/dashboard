from app.data import ProcessedData, DataSource
from typing import List, Dict
import json
from pathlib import Path
import requests

class WeatherDataSource(DataSource):
    def read_location_config() -> List[Dict]: 
        """Read locations from the config file"""
        config_path = Path(__file__).parent.parent / 'configs/locations.json'
        with config_path.open('r') as file:
            locations = json.load(file)
        return locations
    
    def read_api_key() -> Dict:
        config_path = Path(__file__).parent.parent / 'configs/api_keys.json'
        with config_path.open('r') as file:
            locations = json.load(file)
        return locations
    
    def fetch_weather_for_location(name, timezone):
        api_key = "YOUR_API_KEY"
        base_url = "http://api.openweathermap.org/data/2.5/weather"
        params = {
            "q": name,
            "appid": api_key,
            "units": "metric"
        }
        response = requests.get(base_url, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            return None

    def fetch_data(self) -> List[Dict]:
        """Fetch the raw data from an external source."""
        pass

    def process_data(self, raw_data: List[Dict]) -> List[Dict]:
        """Process raw data and extract relevant information."""
        pass

    def get_data(self) -> List[Dict]:
        """Fetch and process data, then return the processed data."""
        raw_data = self.fetch_data()
        processed_data = self.process_data(raw_data)
        return processed_data