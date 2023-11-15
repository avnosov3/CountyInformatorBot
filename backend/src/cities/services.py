from asyncio import sleep

from cities import error_constants
from cities.async_client import city_async_client
from cities.repository import city_repository
from cities.schemas import CityInSchema, CityOutSchema
from core.api_constants import (
    CITIES_API,
    CITY_LIMIT,
    CITY_MIN_POPULATION,
    CITY_ORDER,
    CITY_TYPES,
    REGION_API,
    SLEEP_TIME,
)
from core.error_constants import KEY_ERROR
from core.exceptions import NotFoundError
from countries.repository import country_repository
from countries.schemas import StateInSchema


class CityService:
    def __init__(self):
        self.country_repository = country_repository
        self.city_repository = city_repository
        self.async_client = city_async_client

    async def parse_cities_by_name(
        self,
        name: str,
        url: str = CITIES_API,
        min_population: int = CITY_MIN_POPULATION,
        sort: str = CITY_ORDER,
        types: str = CITY_TYPES,
        limit: str = CITY_LIMIT,
    ) -> list[CityInSchema]:
        """Метод для получения информации о городе от API городов."""
        request_params = dict(
            url=url,
            params=dict(
                minPopulation=min_population,
                namePrefix=name,
                sort=sort,
                types=types,
                limit=limit,
            ),
        )
        cities = await self.async_client.get(**request_params)
        if "data" not in cities:
            raise KeyError(KEY_ERROR.format(**request_params, key="data"))
        return [CityInSchema(**city) for city in cities["data"] if city["name"] == name]

    async def parse_state(self, country: str, region: str) -> StateInSchema:
        """Метод для получения информации о регионе в стране от API городов."""
        url = f"{REGION_API}/{country}/regions/{region}"
        region = await self.async_client.get(url=url)
        if "data" not in region:
            raise KeyError(KEY_ERROR.format(url=url, key="data"))
        return StateInSchema(**region["data"])

    # @cache_handler(cache_name=CitiesConfig.name)
    async def get_cities_by_name(self, name: str) -> list[CityOutSchema]:
        """
        Метод для получения городов по названию.
        Сначала идёт проверка наличия городов в redis.`
        Если города в redis не найдены, то идёт обращение к API городов.
        """
        if await self.city_repository.check_cities_exists_by_name(name):
            cities = await self.city_repository.get_all_citties_by_name_with_states_and_countries(name)
            return [
                CityOutSchema.create(
                    city=city,
                    country=city.state.country,
                    state=city.state,
                )
                for city in cities
            ]

        data = await self.parse_cities_by_name(name)
        output = []
        for city in data:
            country = await self.country_repository.get_country_with_languages_by_code(city.country_code)
            await sleep(SLEEP_TIME)  # API разрешает только одно подключение, поэтому надо подождать :(
            state = await self.parse_state(country.code, city.state_code)
            city, state_db = await self.city_repository.create_or_update_city(city, country, state)
            output.append(CityOutSchema.create(city=city, country=country, state=state_db))
        if not output:
            raise NotFoundError(error_constants.CITY_NOT_FOUND.format(name))
        return output


city_service = CityService()
