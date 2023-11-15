from src.core.client import BaseAsyncClient
from src.core.config import settings
from src.core.exceptions import NotFoundError, StatusCodeNotOKError
from src.weather.schemas import WeatherOutSchema
from src.weather.texts import WEATHER_NOT_FOUND_LOG


class WeatherService:
    def __init__(self):
        self.client = BaseAsyncClient()

    async def get_weather(self, latitude: float, longitude: float) -> WeatherOutSchema:
        try:
            params = dict(latitude=latitude, longitude=longitude)
            data = await self.client.get(url=settings.BACKEND_WEATHER_URL, params=params)
        except StatusCodeNotOKError:
            raise NotFoundError(WEATHER_NOT_FOUND_LOG.format(**params))
        return WeatherOutSchema(**data)
