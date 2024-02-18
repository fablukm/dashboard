from datetime import datetime, timedelta
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
N_CONNECTIONS_FOR_API_CALLS = 50
MAX_TIMEDIFF = timedelta(hours=12)
BASE_URL = "https://search.ch/fahrplan/api/stationboard.json"

@dataclass
class Station:
    name: str
    api_id: int

@dataclass
class Connection:
    line: str
    time: datetime
    terminus: Station
    platform: int
    arrival_time: datetime
    delay: int
    airport: bool

@dataclass
class ConnectionGroup:
    index: int
    transportation_types: List[str]
    show_platform: bool
    n_connections: int
    station_departure: Station
    station_arrival: Station
    connections: List[Connection] = field(default_factory=list)
    airport: Optional[Station] = None

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
        for index, connection in enumerate(connections_json):
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
                index=index,
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
    
    def group_by_departure(self, connection_list_raw: List[ConnectionGroup]) -> Dict:
        '''group the connections by departure'''
        grouped_by_departure = {}
        
        for connection in connection_list_raw:
            key = connection.station_departure.api_id
            if key not in grouped_by_departure:
                grouped_by_departure[key] = []
                grouped_by_departure[key].append(connection)
            else:
                grouped_by_departure[key].append(connection)

        return grouped_by_departure
    
    def call_api(self, station_id: int) -> Dict:
        params = {
            'stop': station_id,
            'limit': N_CONNECTIONS_FOR_API_CALLS,
            'show_subsequent_stops': 1,
            'show_tracks': 1,
            'show_delays': 1
        }

        response = requests.get(BASE_URL, params=params)

        return response

    def extract_data_from_api(self, connection_group: ConnectionGroup, 
                             station_departures: List) -> ConnectionGroup:

        # extract information
        arrival_station = connection_group.station_arrival.api_id

        for departure in station_departures:
            # check if arrival station inside subsequent stops
            is_valid = arrival_station in \
                [int(stop['id']) for stop in departure['subsequent_stops']]
            if not is_valid:
                continue
            else:
                arrival_info = [stop for stop in departure['subsequent_stops'] \
                                if int(stop['id'])==arrival_station][0]

            # check if train type acceptable
            if not departure['type'] in connection_group.transportation_types:
                continue

            # check time
            time_str = departure['time']
            departure_time = datetime.strptime(time_str, DATETIME_API_FORMAT)
            now = datetime.now()
            if departure_time >= now + MAX_TIMEDIFF:
                break
            else:
                departure_time_string = departure_time.strftime("%H:%M")

            # extract arrival time
            arrival_time = datetime.strptime(arrival_info['arr'], DATETIME_API_FORMAT)
            arrival_time_string = arrival_time.strftime("%H:%M")

            # extract delay 
            try:
                delay = int(departure['dep_delay'])
            except Exception:
                delay = 0
            
            # check if this connection has an airport check and perform if necessary
            stops_at_airport = False
            if connection_group.airport:
                airport_station = connection_group.airport['api_id']
                stops_at_airport = airport_station in \
                    [int(stop['id']) for stop in departure['subsequent_stops']]

            # check platform if exists
            try:
                platform = int(departure['track'])
            except KeyError:
                platform = None

            # check terminus
            terminus = Station(name=departure['terminal']['name'], 
                               api_id=int(departure['terminal']['id']))

            # fill in connection object
            this_connection = Connection(line=departure['line'],
                                         time=departure_time_string,
                                         platform=platform,
                                         arrival_time=arrival_time_string,
                                         delay=delay,
                                         airport=stops_at_airport,
                                         terminus=terminus
                                         )
            
            # add parsed connection to ConnectionGroup object
            connection_group.connections.append(this_connection)

            # check break condition and break
            if len(connection_group.connections) >= connection_group.n_connections:
                break

        return connection_group

    def fetch_data(self) -> List[ConnectionGroup]:
        """Fetch the raw data from an external source."""
        # Read connection config
        connection_list = self.read_connections_config()

        # group by departure station to avoid unnecessary API calls
        grouped_by_departure = self.group_by_departure(connection_list)

        output_connections = []
        # get all information by departure station
        for departure_station_id in grouped_by_departure.keys():
            connections_by_departure = grouped_by_departure[departure_station_id]
            api_response = self.call_api(departure_station_id)
            station_departures = api_response.json()['connections']
            for connection_group in connections_by_departure:
                connection_group_parsed = self.extract_data_from_api(connection_group, station_departures)
                output_connections.append(connection_group_parsed)
        return output_connections

    def process_data(self, connection_list: List[ConnectionGroup]) -> List[ConnectionGroup]:
        '''receivs the output of fetch_data and sorts by index'''
        connection_list = sorted(connection_list, key=lambda x: x.index)
        return connection_list
    
if __name__=="__main__":
    tds = TransportDataSource()
    data = tds.get_data()
    print(data)