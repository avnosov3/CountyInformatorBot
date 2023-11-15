from unittest import mock

from django.test import TestCase
from httpx import HTTPError

from core.exceptions import StatusCodeNotOKError
from countries.client import country_client


class TestCountryClient(TestCase):
    @mock.patch("httpx.Client.get")
    def test_raise_error(self, request_get):
        request_get.side_effect = mock.Mock(side_effect=HTTPError("testing"))
        with self.assertRaises(ConnectionError) as context:
            country_client.get_countries()
        self.assertEqual(
            str(context.exception),
            (
                "ENDPOINT: https://restcountries.com/v3.1/all. HEADERS: None. "
                "PARAMS: None. API not avaliable ERROR: testing."
            ),
        )

    @mock.patch("httpx.Client.get")
    def test_error(self, request_get):
        response = mock.Mock()
        response.status_code = 404
        request_get.return_value = response
        with self.assertRaises(StatusCodeNotOKError) as context:
            country_client.get_countries()
        self.assertEqual(
            str(context.exception),
            "ENDPOINT: https://restcountries.com/v3.1/all. HEADERS: None. PARAMS: None. Unexpected return code: 404.",
        )
