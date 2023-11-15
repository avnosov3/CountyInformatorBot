from django.test import TestCase
from django.urls import reverse

API_VERSION = "api-1.0.0"
CITIES = "cities"
CITY_NAME = "Moscow"
PREFIX = "/api/v1"
GET_CITITES_BY_NAME_FUNCTION_NAME = "get_cities_by_name"
CASES = ((f"{PREFIX}/{CITIES}/{CITY_NAME}", GET_CITITES_BY_NAME_FUNCTION_NAME, [CITY_NAME]),)


class CityRoutesTest(TestCase):
    def test_routes(self):
        for obvious, route, args in CASES:
            with self.subTest(obvious=obvious):
                self.assertEqual(obvious, reverse(f"{API_VERSION}:{route}", args=args))
