import requests
from datetime import datetime

def get_weather_data(lat, lon):
    """
    Fetch real-time weather data from OpenWeather API for the given latitude and longitude.
    """
    api_key = 'efa77b8059623abfa65c89700df63858'
    url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=imperial"
    response = requests.get(url)
    data = response.json()

    current_time = datetime.utcfromtimestamp(data['dt'])
    return {  
        'temp': data['main']['temp'],
        'feels_like': data['main']['feels_like'],
        'humidity': data['main']['humidity'],
        'wind_speed': data['wind']['speed'],
        'clouds_all': data['clouds']['all'],
        'weather_description': data['weather'][0]['description'],
        'DayOfWeek': current_time.weekday(),
        'Hour': current_time.hour
    }
