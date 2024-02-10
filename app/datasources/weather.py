from data import ProcessedData, DataSource
from typing import List, Dict
import json
from pathlib import Path
from dataclasses import dataclass
import requests

@dataclass
class Location:
    name: str
    timezone: str
    lat: float
    lon: float

class WeatherDataSource(DataSource):
    def read_location_config(self) -> List[Dict]: 
        """Read locations from the config file"""
        config_path = Path(__file__).parent.parent.parent / 'configs/locations.json'
        with config_path.open('r') as file:
            locations = json.load(file)
        return locations
    
    def read_api_key(self) -> Dict:
        config_path = Path(__file__).parent.parent.parent / 'configs/api_keys.json'
        with config_path.open('r') as file:
            api_keys = json.load(file)
        osm_api_key = [value for value in api_keys if value["service"]=="OpenWeatherMaps"][0]
        return osm_api_key["key"]
    
    def fetch_weather_for_location(self, location):
        api_key = self.read_api_key()
        base_url = "http://api.openweathermap.org/data/2.5/weather"
        params = {
            "lat": location["lat"],
            "lon": location["lon"],
            "appid": api_key,
            "units": "metric",
            "exclude": "daily,minutely,alerts",
        }

        response = requests.get(base_url, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            return None

    def fetch_data(self) -> List[Dict]:
        """Fetch the raw data from an external source."""
        locations = self.read_location_config()

        weather_results = []
        for loc in locations:
            response = self.fetch_weather_for_location(loc)
            result = {
                "name": loc["name"],
                "raw_info": loc,
                "weather": response
                }
            
        pass

    def process_data(self, raw_data: List[Dict]) -> List[Dict]:
        """Process raw data and extract relevant information."""
        pass

    def get_data(self) -> List[Dict]:
        """Fetch and process data, then return the processed data."""
        raw_data = self.fetch_data()
        processed_data = self.process_data(raw_data)
        return processed_data
    
if __name__=="__main__":
    wds = WeatherDataSource()
    print(wds.fetch_data())