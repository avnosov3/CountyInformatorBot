from core.api_constants import WEATHER_API_KEY, WEATHER_API_TOKEN, WEATHER_API_URL
from core.async_client import BaseAsyncClient
from weather.schemas import WeatherSchema


class WeatherAsyncClient(BaseAsyncClient):
    """Клиент для работы с API погоды."""

    def __init__(self):
        headers = {WEATHER_API_KEY: WEATHER_API_TOKEN}
        super().__init__(headers=headers)

    async def get_weather(self, lat: float, lon: float, url: str = WEATHER_API_URL) -> WeatherSchema:
        weather = await self.get(url, params=dict(lat=lat, lon=lon))
        return WeatherSchema(**weather)


weather_async_client = WeatherAsyncClient()
