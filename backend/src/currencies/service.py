from django.core.cache import caches

from core.exceptions import NotFoundError
from countries.repository import country_repository
from currencies import error_constants
from currencies.schemas import CurrencyOutSchema


class CurrencyService:
    def __init__(self):
        self.country_repository = country_repository
        self.currency_cache = caches["currencies"]

    async def get_exchange_rate(self, code: str) -> CurrencyOutSchema:
        exchange_rate = await self.currency_cache.aget(code)
        if exchange_rate is None:
            raise NotFoundError(error_constants.CURRENCY_EXCHANGE_RATE_NOT_FOUND.format(code))
        return CurrencyOutSchema(exchange_rate=exchange_rate)


currency_service = CurrencyService()
