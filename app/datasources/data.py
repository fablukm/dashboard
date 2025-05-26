from .weather import WeatherDataSource
from .transport import TransportDataSource

def get_dashboard_data():
    # transport
    transport_data_source = TransportDataSource()
    transport_data = transport_data_source.get_data()

    # weather
    weather_data_source = WeatherDataSource()
    weather_data = weather_data_source.get_data()

    dashbard_api_response = {
        "weather": weather_data,
        "events": [
            {"name": "Meeting with team", "time": "11:00 AM"},
            {"name": "Doctor's Appointment", "time": "3:00 PM"}
        ],
        "unread_emails": 5,
        "public_transport": transport_data
    }
    return dashbard_api_response