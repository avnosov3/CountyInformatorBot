from src.core.client import BaseAsyncClient
from src.core.config import settings
from src.core.exceptions import NotFoundError, StatusCodeNotOKError
from src.countries.schemas import CountryOutSchema
from src.countries.texts import COUNTY_NOT_FOUND


class CountryService:
    def __init__(self):
        self.client = BaseAsyncClient()

    async def get_country_by_name(self, name: str) -> CountryOutSchema:
        try:
            country = await self.client.get(f"{settings.BACKEND_COUNTRY_URL}/{name}")
        except StatusCodeNotOKError:
            raise NotFoundError(COUNTY_NOT_FOUND.format(name=name))
        return CountryOutSchema.create_output(country)
