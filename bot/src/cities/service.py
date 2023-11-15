from src.cities.schemas import CityOutSchema, StateOutSchema
from src.cities.texts import CITY_NOT_FOUND
from src.core.client import BaseAsyncClient
from src.core.config import settings
from src.core.exceptions import NotFoundError, StatusCodeNotOKError


class CityService:
    def __init__(self):
        self.client = BaseAsyncClient()

    async def get_cities(self, name: str) -> dict:
        try:
            datas = await self.client.get(f"{settings.BACKEND_CITY_URL}/{name}")
        except StatusCodeNotOKError:
            raise NotFoundError(CITY_NOT_FOUND.format(name=name))
        return datas

    async def get_cities_by_name(self, name: str) -> list[CityOutSchema]:
        cities = await self.get_cities(name)
        return [CityOutSchema.create_output(city) for city in cities]

    async def get_city_by_region(self, city_name: str, region: str) -> list[CityOutSchema]:
        cities = await self.get_cities(city_name)
        return [CityOutSchema.create_output(city) for city in cities if city["state"]["name"] == region]

    async def get_regions(self, city_name: str, country: str) -> list[StateOutSchema]:
        cities = await self.get_cities(city_name)
        return [city["state"]["name"] for city in cities if city["country"]["name"] == country]
