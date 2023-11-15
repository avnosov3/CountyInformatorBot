from core import error_constants
from core.api_constants import CURRENCY_API, CURRENCY_API_KEY, CURRENCY_API_TOKEN
from core.sync_client import BaseSyncClient


class CurrencyClient(BaseSyncClient):
    """Клиент для работы с API валют. Будет использоваться в celery beat."""

    def get_currencies(self) -> dict:
        request_params = dict(
            url=CURRENCY_API,
            params={CURRENCY_API_KEY: CURRENCY_API_TOKEN},
        )
        data = self.get(**request_params)
        if "quotes" not in data:
            raise KeyError(error_constants.KEY_ERROR.format(**request_params, headers=self.headers, key="quotes"))
        return data["quotes"]


currency_client = CurrencyClient()
