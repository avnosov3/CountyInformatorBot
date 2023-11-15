from unittest import mock

from django.test import TestCase
from httpx import HTTPError

from cities.async_client import city_async_client
from core.exceptions import StatusCodeNotOKError


class TestCityClient(TestCase):
    @mock.patch("httpx.AsyncClient.get")
    async def test_raise_error(self, request_get):
        request_get.side_effect = mock.Mock(side_effect=HTTPError("testing"))
        with self.assertRaises(ConnectionError) as context:
            await city_async_client.get(url="test_url")
        self.assertEqual(
            str(context.exception),
            (
                "ENDPOINT: test_url. "
                "HEADERS: {'X-RapidAPI-Key': '687a148ee8mshf9056d5f3c67e67p1ed2d6jsn65fbed7779a5', "
                "'X-RapidAPI-Host': 'wft-geo-db.p.rapidapi.com'}. "
                "PARAMS: None. API not avaliable ERROR: testing."
            ),
        )

    @mock.patch("httpx.AsyncClient.get")
    async def test_invalid_status_code(self, request_get):
        response = mock.Mock()
        response.status_code = 404
        request_get.return_value = response
        with self.assertRaises(StatusCodeNotOKError) as context:
            await city_async_client.get(url="test_url")
        self.assertEqual(
            str(context.exception),
            (
                "ENDPOINT: test_url. "
                "HEADERS: {'X-RapidAPI-Key': '687a148ee8mshf9056d5f3c67e67p1ed2d6jsn65fbed7779a5', "
                "'X-RapidAPI-Host': 'wft-geo-db.p.rapidapi.com'}. "
                "PARAMS: None. Unexpected return code: 404."
            ),
        )
