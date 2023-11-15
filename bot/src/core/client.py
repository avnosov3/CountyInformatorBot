import logging

from httpx import AsyncClient, HTTPError
from httpx._status_codes import code as status_code

from src.core import error_constants, exceptions
from src.core.config import settings


class BaseAsyncClient:
    def __init__(self, headers: dict | None = None):
        self.async_client = AsyncClient()
        self.headers = headers

    async def get(self, url: str, params: dict | None = None) -> dict:
        request_params = dict(url=url, params=params, headers=self.headers)
        try:
            response = await self.async_client.get(url=url, params=params, timeout=settings.CLIENT_TIMEOUT)
        except HTTPError as error:
            message = error_constants.API_NOT_AVALIABLE.format(**request_params, error=error)
            logging.exception(message)
            raise ConnectionError(message)
        response_status_code = response.status_code
        if response_status_code != status_code.OK:
            message = error_constants.STATUS_CODE_ERROR.format(**request_params, status_code=response_status_code)
            logging.exception(message)
            raise exceptions.StatusCodeNotOKError(message)
        return response.json()
