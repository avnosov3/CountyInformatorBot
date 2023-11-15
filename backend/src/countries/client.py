from core.api_constants import COUNTRIES_API
from core.sync_client import BaseSyncClient
from countries.schemas import CountryInSchema


class CountryClient(BaseSyncClient):
    "Клиент для работы с API стран. Будет использоваться в celery beat."

    def get_countries(self) -> list[CountryInSchema]:
        """Метод для отбора определенных стран, так как в API есть вымышленные страны."""
        return [
            CountryInSchema.parse(country_in)
            for country_in in self.get(COUNTRIES_API)
            if country_in.get("languages") is not None
            and country_in.get("area", 0) > 0
            and country_in.get("population", 0) > 0
        ]


country_client = CountryClient()
