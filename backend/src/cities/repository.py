import datetime

import pytz
from asgiref.sync import sync_to_async
from django.db.models import Prefetch
from timezonefinder import TimezoneFinder

from cities.apps import CitiesConfig
from cities.models import City
from cities.schemas import CityInSchema
from core.cache import cache_handler
from countries.models import Country, State
from countries.repository import country_repository
from countries.schemas import StateInSchema


class CityRepository:
    def __init__(self, city=City, state=State):
        self.country_repository = country_repository
        self.city = city
        self.state = state
        self.timezone_finder = TimezoneFinder()

    async def create_or_update_state(self, state: StateInSchema, country: Country) -> State:
        state, _ = await self.state.objects.aupdate_or_create(
            country=country, code=state.code, defaults={**state.dict(exclude={"code"})}
        )
        return state

    def convert_coordinates_to_utc(self, city: CityInSchema) -> str:
        timezone = self.timezone_finder.timezone_at(lng=city.longitude, lat=city.latitude)
        utc = datetime.datetime.now(pytz.timezone(timezone)).strftime("%z")
        hours, minutes = utc[:3], utc[3:]
        return f"{hours}:{minutes}"

    async def create_or_update_city(
        self, city: CityInSchema, country: Country, state: StateInSchema
    ) -> tuple[City, State]:
        state = await self.create_or_update_state(state, country)
        utc = self.convert_coordinates_to_utc(city)
        city, _ = await self.city.objects.aupdate_or_create(
            latitude=city.latitude,
            longitude=city.longitude,
            defaults={
                "state": state,
                "utc": utc,
                **city.dict(
                    exclude={"state_code", "country_code", "longitude", "latitude"},
                ),
            },
        )
        return city, state

    async def check_cities_exists_by_name(self, name: str) -> bool:
        return await self.city.objects.filter(name=name).aexists()

    @cache_handler(cache_name=CitiesConfig.name)
    async def get_all_citties_by_name_with_states_and_countries(self, name: str) -> City:
        return await sync_to_async(list)(
            self.city.objects.select_related("state__country", "state__country__currency", "state__country__continent")
            .prefetch_related(Prefetch("state__country__languages", to_attr="all_languages"))
            .filter(name__iexact=name)
            .all()
        )


city_repository = CityRepository()
