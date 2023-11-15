from src.core.client import BaseAsyncClient
from src.core.config import settings
from src.core.exceptions import NotFoundError, StatusCodeNotOKError
from src.currencies.schemas import CurrencyOutSchema
from src.currencies.texts import CURRENCY_NOT_FOUND


class CurrencyService:
    def __init__(self):
        self.client = BaseAsyncClient()

    async def get_currency_by_name(self, name: str) -> CurrencyOutSchema:
        try:
            currency_exchange_rate = await self.client.get(f"{settings.BACKEND_CURRENCY_URL}{name}")
        except StatusCodeNotOKError:
            raise NotFoundError(CURRENCY_NOT_FOUND.format(name=name))
        return CurrencyOutSchema(**currency_exchange_rate, name=name)
