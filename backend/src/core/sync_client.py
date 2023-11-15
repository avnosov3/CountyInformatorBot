from httpx import Client, HTTPError
from httpx._status_codes import code as status_code

from core import error_constants, exceptions


class BaseSyncClient:
    def __init__(self, headers: dict | None = None):
        self.sync_client = Client()
        self.headers = headers

    def get(self, url: str, params: dict | None = None) -> dict:
        request_params = dict(
            url=url,
            headers=self.headers,
            params=params,
        )
        try:
            response = self.sync_client.get(url=url, headers=self.headers, params=params)
        except HTTPError as error:
            raise ConnectionError(error_constants.API_NOT_AVALIABLE.format(**request_params, error=error))
        response_status_code = response.status_code
        if response_status_code != status_code.OK:
            raise exceptions.StatusCodeNotOKError(
                error_constants.STATUS_CODE_ERROR.format(**request_params, status_code=response_status_code)
            )
        return response.json()
