from asgiref.sync import sync_to_async
from django.core.cache import caches
from django.db.models import Prefetch
from django.test import AsyncClient, TestCase
from django.urls import reverse
from httpx._status_codes import code as status_code

from cities.models import City
from cities.tests.factories import CityFactory
from cities.tests.test_cities_router import API_VERSION, GET_CITITES_BY_NAME_FUNCTION_NAME
from countries.models import Country
from countries.tests.factories import CountryFactory, LanguageFactory, StateFactory


class CityEndpointTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.country = CountryFactory.create(code=1, phone_code=1, languages=(LanguageFactory(),))
        cls.state = StateFactory.create(country=cls.country)
        cls.city = CityFactory.create(state=cls.state)
        cls.CITY_BY_NAME_URL = reverse(f"{API_VERSION}:{GET_CITITES_BY_NAME_FUNCTION_NAME}", args=[cls.city.name])
        cls.country = (
            Country.objects.select_related(
                "continent",
                "currency",
            )
            .prefetch_related("languages")
            .filter(name=cls.country.name)
            .first()
        )
        cls.cities = sync_to_async(list)(
            City.objects.select_related("state__country", "state__country__currency", "state__country__continent")
            .prefetch_related(Prefetch("state__country__languages", to_attr="all_languages"))
            .filter(name=cls.city.name)
            .all()
        )

    def setUp(self):
        self.guest = AsyncClient()
        for cache in caches.all():
            cache.clear()

    async def test_get_city_by_name_output(self):
        response = await self.guest.get(self.CITY_BY_NAME_URL)
        data = response.json()
        first_city, *_ = data
        country = first_city["country"]
        state = first_city["state"]
        self.assertEqual(response.status_code, status_code.OK)
        for city in await self.cities:
            for value, excepted in (
                (first_city["name"], city.name),
                (first_city["code"], city.code),
                (first_city["population"], city.population),
                (first_city["latitude"], city.latitude),
                (first_city["longitude"], city.longitude),
                (first_city["utc"], city.utc),
                (country["name"], self.country.name),
                (country["code"], self.country.code),
                (country["phone_code"], self.country.phone_code),
                (country["currency"], self.country.currency.code),
                (country["languages"], [language.name for language in self.country.languages.all()]),
                (state["name"], city.state.name),
                (state["num_cities"], city.state.num_cities),
                (state["code"], city.state.code),
            ):
                self.assertEqual(value, excepted)
