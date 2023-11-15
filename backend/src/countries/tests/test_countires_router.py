from django.test import TestCase
from django.urls import reverse

API_VERSION = "api-1.0.0"
COUNTRIES = "countries"
COUNTRY_NAME = "Russia"
PREFIX = "/api/v1"
GET_COUNTRY_BY_NAME_FUNCTION_NAME = "get_country_by_name"
CASES = ((f"{PREFIX}/{COUNTRIES}/{COUNTRY_NAME}", GET_COUNTRY_BY_NAME_FUNCTION_NAME, [COUNTRY_NAME]),)


class CountryRoutesTest(TestCase):
    def test_routes(self):
        for obvious, route, args in CASES:
            with self.subTest(obvious=obvious):
                self.assertEqual(obvious, reverse(f"{API_VERSION}:{route}", args=args))
