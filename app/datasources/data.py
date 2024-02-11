from .weather import WeatherDataSource

def get_dashboard_data():
    # weather
    weather_data_source = WeatherDataSource()
    weather_data = weather_data_source.get_data()

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