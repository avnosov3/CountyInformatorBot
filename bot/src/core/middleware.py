from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject


class ServiceMiddleware(BaseMiddleware):
    def __init__(self, country_service, currency_service, city_service, weather_service):
        self.country_service = country_service
        self.currency_service = currency_service
        self.city_service = city_service
        self.weather_service = weather_service

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        data["country_service"] = self.country_service
        data["currency_service"] = self.currency_service
        data["city_service"] = self.city_service
        data["weather_service"] = self.weather_service
        return await handler(event, data)
