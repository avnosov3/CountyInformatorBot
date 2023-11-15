import asyncio
import logging
from logging.handlers import RotatingFileHandler

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage
from redis.asyncio import Redis

from src.cities.handlers import cities_router
from src.cities.service import CityService
from src.core.config import settings
from src.core.middleware import ServiceMiddleware
from src.countries.handlers import countries_router
from src.countries.service import CountryService
from src.currencies.handlers import currency_router
from src.currencies.service import CurrencyService
from src.menu.handlers import menu_router
from src.unexcepted_behaviour.handlers import unexcepted_behavior
from src.weather.handlers import weather_router
from src.weather.service import WeatherService

rotating_handler = RotatingFileHandler(filename="bot.log", maxBytes=10**6, backupCount=5, encoding="utf-8")
logging.basicConfig(
    datefmt="%d.%m.%Y %H:%M:%S",
    format='"%(asctime)s - [%(levelname)s] - %(message)s"',
    level=logging.ERROR,
    handlers=(rotating_handler, logging.StreamHandler()),
)


async def main() -> None:
    bot = Bot(token=settings.BOT_API_TOKEN, parse_mode=ParseMode.HTML)
    dispatcher = Dispatcher(
        storage=RedisStorage(Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.BOT_REDIS_DB))
    )
    dispatcher.message.middleware(
        ServiceMiddleware(CountryService(), CurrencyService(), CityService(), WeatherService())
    )
    dispatcher.callback_query.middleware(
        ServiceMiddleware(CountryService(), CurrencyService(), CityService(), WeatherService())
    )
    # dispatcher.include_router(unexcepted_behavior)
    dispatcher.include_router(menu_router)
    dispatcher.include_router(countries_router)
    dispatcher.include_router(currency_router)
    dispatcher.include_router(cities_router)
    dispatcher.include_router(weather_router)
    dispatcher.include_router(unexcepted_behavior)
    await dispatcher.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
