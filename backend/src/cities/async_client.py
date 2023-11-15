from core.api_constants import CITY_API_HOST_KEY, CITY_API_HOST_VALUE, CITY_API_KEY, CITY_API_KEY_VALUE
from core.async_client import BaseAsyncClient


class CityAsyncClient(BaseAsyncClient):
    """Клиент для работы с API городов."""

    def __init__(self):
        headers = {CITY_API_KEY: CITY_API_KEY_VALUE, CITY_API_HOST_KEY: CITY_API_HOST_VALUE}
        super().__init__(headers=headers)


city_async_client = CityAsyncClient()
