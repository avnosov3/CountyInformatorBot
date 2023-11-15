from django.core.cache import caches
from django.test import AsyncClient, TestCase
from django.urls import reverse
from httpx._status_codes import code as status_code

from countries.models import Country
from countries.tests import factories
from countries.tests.test_countires_router import API_VERSION, GET_COUNTRY_BY_NAME_FUNCTION_NAME

UNEXISTING_COUNTRY_BY_NAME_URL = reverse(f"{API_VERSION}:{GET_COUNTRY_BY_NAME_FUNCTION_NAME}", args=["Country"])


class CountryEndpointTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.country = factories.CountryFactory.create(code=1, phone_code=1, languages=(factories.LanguageFactory(),))
        cls.COUNTRY_BY_NAME_URL = reverse(f"{API_VERSION}:{GET_COUNTRY_BY_NAME_FUNCTION_NAME}", args=[cls.country.name])
        cls.country_with_languages = (
            Country.objects.select_related(
                "continent",
                "currency",
            )
            .prefetch_related("languages")
            .filter(name=cls.country.name)
            .first()
        )

    def setUp(self):
        self.guest = AsyncClient()
        for cache in caches.all():
            cache.clear()

    async def test_get_country_by_name_output(self):
        response = await self.guest.get(self.COUNTRY_BY_NAME_URL)
        data = response.json()
        self.assertEqual(response.status_code, status_code.OK)
        self.assertEqual(data["name"], self.country_with_languages.name)
        for value, excepted in (
            (data["name"], self.country_with_languages.name),
            (data["full_name"], self.country_with_languages.full_name),
            (data["capital"], self.country_with_languages.capital),
            (data["continent"], self.country_with_languages.continent.name),
            (data["population"], self.country_with_languages.population),
            (data["size"], self.country_with_languages.size),
            (data["code"], self.country_with_languages.code),
            (data["phone_code"], self.country_with_languages.phone_code),
            (data["currency"], self.country_with_languages.currency.code),
            (data["languages"], [language.name for language in self.country_with_languages.languages.all()]),
        ):
            self.assertEqual(value, excepted)
