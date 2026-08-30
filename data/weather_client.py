import os
import logging
import requests
from typing import Dict, Any, Optional

# Setup logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# WMO Weather interpretation codes (https://open-meteo.com/en/docs)
WEATHER_CODES: Dict[int, str] = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Foggy",
    48: "Depositing rime fog",
    51: "Light drizzle",
    53: "Moderate drizzle",
    55: "Dense drizzle",
    56: "Light freezing drizzle",
    57: "Dense freezing drizzle",
    61: "Slight rain",
    63: "Moderate rain",
    65: "Heavy rain",
    66: "Light freezing rain",
    67: "Heavy freezing rain",
    71: "Slight snow fall",
    73: "Moderate snow fall",
    75: "Heavy snow fall",
    77: "Snow grains",
    80: "Slight rain showers",
    81: "Moderate rain showers",
    82: "Violent rain showers",
    85: "Slight snow showers",
    86: "Heavy snow showers",
    95: "Thunderstorm",
    96: "Thunderstorm with slight hail",
    99: "Thunderstorm with heavy hail"
}

def get_weather_forecast(lat: float, lon: float) -> Dict[str, Any]:
    """
    Fetches real-time weather information for given latitude and longitude coordinates
    using the Open-Meteo API.
    
    Args:
        lat (float): Latitude coordinate.
        lon (float): Longitude coordinate.
        
    Returns:
        dict: A structured dictionary containing weather conditions and suitability flags.
    """
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "current": "temperature_2m,relative_humidity_2m,precipitation,weather_code,wind_speed_10m",
        "timezone": "auto"
    }
    
    # Check if a custom WEATHER_API_KEY is available (in case the team wants to switch providers/auth in future)
    api_key = os.getenv("WEATHER_API_KEY")
    if api_key:
        logger.info("Custom WEATHER_API_KEY detected. (Open-Meteo does not require a key, proceeding using free tier).")

    try:
        logger.info(f"Fetching weather data for Coordinates: ({lat}, {lon})")
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        current = data.get("current", {})
        temp = current.get("temperature_2m")
        humidity = current.get("relative_humidity_2m")
        precipitation = current.get("precipitation", 0.0)
        wind_speed = current.get("wind_speed_10m")
        weather_code = current.get("weather_code", 0)
        
        condition = WEATHER_CODES.get(weather_code, f"Unknown ({weather_code})")
        
        # Crop safety metrics
        # Heavy rain (weather code >= 63), Snow, Drizzle, or Thunderstorm can impact harvesting and transport.
        is_rainy = weather_code in [61, 63, 65, 66, 67, 80, 81, 82]
        is_stormy = weather_code in [95, 96, 99]
        is_snowy = weather_code in [71, 73, 75, 77, 85, 86]
        is_foggy = weather_code in [45, 48]
        
        is_suitable_for_harvest = not (is_rainy or is_stormy or is_snowy)
        is_suitable_for_transport = not (is_stormy or is_snowy or is_foggy or (is_rainy and precipitation > 5.0))
        
        result = {
            "status": "success",
            "latitude": lat,
            "longitude": lon,
            "temperature_celsius": temp,
            "humidity_percentage": humidity,
            "wind_speed_kmh": wind_speed,
            "precipitation_mm": precipitation,
            "weather_code": weather_code,
            "condition": condition,
            "is_suitable_for_harvest": is_suitable_for_harvest,
            "is_suitable_for_transport": is_suitable_for_transport
        }
        logger.info(f"Successfully retrieved weather condition: {condition}")
        return result

    except requests.RequestException as e:
        logger.error(f"Error fetching weather data: {e}")
        return {
            "status": "error",
            "message": str(e),
            "latitude": lat,
            "longitude": lon,
            "temperature_celsius": None,
            "humidity_percentage": None,
            "wind_speed_kmh": None,
            "precipitation_mm": None,
            "weather_code": None,
            "condition": "Error retrieving weather",
            "is_suitable_for_harvest": True,  # Fallback gracefully
            "is_suitable_for_transport": True
        }
