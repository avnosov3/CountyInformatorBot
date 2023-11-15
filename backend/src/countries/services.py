from core.cache import cache_handler
from core.exceptions import NotFoundError
from countries import error_constants
from countries.apps import CountriesConfig
from countries.repository import country_repository
from countries.schemas import CountryOutSchema


class CountryService:
    def __init__(self):
        self.country_repository = country_repository

    @cache_handler(cache_name=CountriesConfig.name)
    async def get_country_by_name(self, name: str) -> CountryOutSchema:
        country = await self.country_repository.get_country_with_languages_by_name(name)
        if country is None:
            raise NotFoundError(error_constants.COUNTRY_NOT_FOUND.format(name))
        return CountryOutSchema.create(country)


country_service = CountryService()
