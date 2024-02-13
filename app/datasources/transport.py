from datetime import datetime
import requests
import json
from pathlib import Path
from dataclasses import dataclass, field
from typing import List, Dict, Tuple, Optional

try:
    # Try to import using the package path (as if it's part of a larger application)
    from .datasource import DataSource
except ImportError:
    # Fall back to a direct import if the relative import fails (likely running standalone)
    from datasource import DataSource
    
DATETIME_API_FORMAT = r"%Y-%m-%d %H:%M:%S"
DATETIME_OUTPUT_FORMAT = r"%H:%M"
N_CONNECTIONS_FOR_API_CALLS = 30
BASE_URL = "https://search.ch/fahrplan/api/stationboard.json"

@dataclass
class Station:
    name: str
    api_id: int

@dataclass
class Connection:
    symbol_id: str
    time: datetime
    platform: int
    arrival_time: datetime
    delay: int
    arrival_delay: int
    airport: bool

@dataclass
class ConnectionGroup:
    transportation_types: str
    show_platform: bool
    n_connections: int
    station_departure: Station
    station_arrival: Station
    connections: List[Connection] = field(default_factory=list)
    airport: Optional[Station] = None
    _api_response: Optional[dict] = None

class TransportDataSource(DataSource):
    def read_connections_config(self) -> List[ConnectionGroup]:
        """Read locations from the config file"""
        config_path = Path(__file__).parent.parent.parent / 'configs/transport.json'
        with config_path.open('r') as file:
            connections_json = json.load(file)

        connection_list_empty = self.parse_connections(connections_json=connections_json)

        return connection_list_empty
    
    def parse_connections(self, connections_json: List[Dict]) -> List[ConnectionGroup]:
        
        # initialize
        connection_list_empty = []

        # parse
        for connection in connections_json:
            # read all info and save it in the structure
            station_departure = Station(
                name=connection['from']['name'],
                api_id=connection['from']['api_id']
            )
            station_arrival = Station(
                name=connection['to']['name'],
                api_id=connection['to']['api_id']
            )
            connection_group = ConnectionGroup(
                transportation_types=connection['info']['transportation_types'],
                show_platform=connection['info']['show_platform'],
                n_connections=connection['info']['n_connections'],
                station_departure=station_departure,
                station_arrival=station_arrival
            )

            # read airport if there is one
            try:
                connection_group.airport = connection['info']['airport']
            except KeyError:
                connection_group.airport = None

            connection_list_empty.append(connection_group)
        return connection_list_empty
    
    def call_api(self, connection: ConnectionGroup) -> Dict:
        params = {
            'stop': connection.station_departure.api_id,
            'limit': N_CONNECTIONS_FOR_API_CALLS,
            'transportation_types': connection.transportation_types,
            'show_subsequent_stops': 1,
            'show_tracks': 1,
            'show_delays': 1
        }

        response = requests.get(BASE_URL, params=params)

        return response.json()

    def format_response(self, connection_group: ConnectionGroup) -> None:
        # extract matching connections from api response
        connections = [con for con in connection_group._api_response['connections'] \
            if True in [stop['id']==str(connection_group.station_arrival.api_id) \
                        for stop in con['subsequent_stops']]]

        return

    def fetch_data(self) -> List[ConnectionGroup]:
        """Fetch the raw data from an external source."""
        # Read connection config
        connection_list_raw = self.read_connections_config()

        # loop through all connections and call the api to get the info. Attach it to the object
        for connection_raw in connection_list_raw:
            # TODO: merge departure stations together and avoid multiple calls for the same stationboard
            this_response = self.call_api(connection_raw)
            connection_raw._api_response = this_response

        return connection_list_raw

    def process_data(self, connection_list: List[ConnectionGroup]) -> List[ConnectionGroup]:
        '''formats the api responses to the required data structure'''

        for connection_group in connection_list:
            self.format_response(connection_group=connection_group)

        return connection_list
    
if __name__=="__main__":
    tds = TransportDataSource()
    print(tds.get_data())