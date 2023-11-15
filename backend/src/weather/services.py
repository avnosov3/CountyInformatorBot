from core.cache import cache_handler
from weather.apps import name as weather_app
from weather.async_client import weather_async_client
from weather.schemas import WeatherSchema


class WeatherService:
    def __init__(self):
        self.weather_client = weather_async_client

    @cache_handler(cache_name=weather_app)
    async def get_weather_by_coordinates(self, lat: float, lon: float) -> WeatherSchema:
        return await weather_async_client.get_weather(lat, lon)


weather_service = WeatherService()
