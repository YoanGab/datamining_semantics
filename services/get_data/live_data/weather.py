import requests
from dotenv import load_dotenv
from services.utils.utils import convert_kelvin_to_celsius
import os


def get_temperature(latitude: float, longitude: float) -> float:
    """
    Returns the current temperature in Celsius for the given latitude and longitude.
    """
    return 0
    load_dotenv()
    api_key = os.getenv("WEATHER_API_KEY")
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={api_key}&units=metric"
    response = requests.get(url)
    data = response.json()
    return convert_kelvin_to_celsius(data["main"]["temp"])
