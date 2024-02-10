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