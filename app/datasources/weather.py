from datetime import datetime
from typing import List, Dict
import json
from pathlib import Path
from dataclasses import dataclass
import requests
from .datasource import DataSource

@dataclass
class Location:
    name: str
    timezone: str
    lat: float
    lon: float

@dataclass
class WeatherResult:
    location: Dict
    response: Dict
    timestamp: str
    WeatherId: int
    WeatherIcon: str
    Temperature: float
    TemperatureFeelsLike: float
    WindSpeed: float

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
        osm_api_key = api_keys["OpenWeatherMaps"]
        return osm_api_key["key"]
    
    def fetch_weather_for_location(self, location):
        api_key = self.read_api_key()
        base_url = "http://api.openweathermap.org/data/2.5/weather"
        params = {
            "q": location["name"],
            "appid": api_key,
            "units": "metric",
            "exclude": "daily,minutely,alerts",
        }

        response = requests.get(base_url, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            return None

    def fetch_data(self) -> List[WeatherResult]:
        """Fetch the raw data from an external source."""
        locations = self.read_location_config()

        weather_results = []
        for loc in locations:
            response = self.fetch_weather_for_location(loc)
            
            try:
                result = WeatherResult(location=loc,
                                       response=response, 
                                       timestamp=datetime.now().__str__(),
                                       WeatherId=response['weather'][0]['id'],
                                       WeatherIcon=response['weather'][0]['icon'],
                                       Temperature=round(response['main']['temp']),
                                       TemperatureFeelsLike=response['main']['feels_like'],
                                       WindSpeed=response['wind']['speed']
                                       )
            except:
                result = WeatherResult(location=loc,
                                       response=response, 
                                       timestamp=datetime.now().__str__(),
                                       WeatherId=0,
                                       WeatherIcon='',
                                       Temperature=0,
                                       TemperatureFeelsLike=0,
                                       WindSpeed=0
                                       )
            weather_results.append(result)
            
        return weather_results

    def process_data(self, response_data: List[WeatherResult]) -> List[Dict]:
        api_response = {
            "location": response_data[0].location['displayname'],
            "weather_icon": response_data[0].WeatherIcon,
            "weatherId": response_data[0].WeatherId,
            "temp": response_data[0].Temperature,
            "additional_locations": [
                {"location": response_data[1].location['displayname'], 
                 "weather_icon": response_data[1].WeatherIcon, 
                 "weatherId": response_data[1].WeatherId,
                 "temp": response_data[1].Temperature
                 },
                {"location": response_data[2].location['displayname'], 
                 "weather_icon": response_data[2].WeatherIcon, 
                 "weatherId": response_data[2].WeatherId,
                 "temp": response_data[2].Temperature
                 }
            ]
            }

        return api_response
    
if __name__=="__main__":
    wds = WeatherDataSource()
    print(wds.get_data())