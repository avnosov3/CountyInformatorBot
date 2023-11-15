from django.db.models import Prefetch, Q

from countries.models import Continent, Country, Language
from countries.schemas import CountryInSchema
from currencies.models import Currency


class CountryRepository:
    def __init__(self, country=Country, continent=Continent, language=Language, currency=Currency):
        self.country = country
        self.continent = continent
        self.language = language
        self.currency = currency

    def prepare_country_and_create_or_get_continent_and_currency(
        self, country_in: CountryInSchema, update: bool = False
    ) -> Country | dict:
        """
        Вспомогающий метод, который будет использоваться в функцях create_country, update_country,
        которые будут использоваться в celery beat.
        """
        continent_db, _ = self.continent.objects.get_or_create(name=country_in.continent)
        currency_db, _ = self.currency.objects.get_or_create(code=country_in.currency)
        kwargs = dict(
            name=country_in.name,
            full_name=country_in.full_name,
            capital=country_in.capital,
            continent=continent_db,
            population=country_in.population,
            size=country_in.size,
            code=country_in.code,
            phone_code=country_in.phone_code,
            currency=currency_db,
        )
        if update:
            del kwargs["code"]
            return kwargs
        return self.country(**kwargs)

    def create_languages(self, countries_in: list[CountryInSchema]) -> list[Language]:
        """
        Вспомогающий метод, который будет использоваться в функциях create_country, update_country,
        которые будут использоваться в celery beat.
        """
        languages = set()
        for country_in in countries_in:
            for language in country_in.languages:
                languages.add(language)
        self.language.objects.bulk_create(
            [self.language(name=language) for language in languages], ignore_conflicts=True
        )
        return self.language.objects.all()

    def set_languages_in_countries(
        self, countries_in: list[CountryInSchema], countries_db: list[Country]
    ) -> list[Country]:
        """
        Вспомогающий метод, который будет использоваться в функциях create_country, update_country,
        которые будут использоваться в celery beat.
        """
        languages_db = self.create_languages(countries_in)
        for country_in, updated_country in zip(countries_in, countries_db):
            updated_country.languages.set(
                [language_db for language_db in languages_db if language_db.name in country_in.languages]
            )
        return countries_db

    def create_countries(self, countries_in: list[CountryInSchema]) -> list[Country]:
        """Создание стран со всеми вложенными связями. Метод будет использоваться в celery beat."""
        self.country.objects.bulk_create(
            [self.prepare_country_and_create_or_get_continent_and_currency(country_in) for country_in in countries_in],
            ignore_conflicts=True,
        )
        created_countries = self.country.objects.all()
        return self.set_languages_in_countries(countries_in, created_countries)

    def update_countries(self, countries_in: list[CountryInSchema]) -> list[Country]:
        """Обновление стран со всеми вложенными связями. Метод будет использоваться в celery beat."""
        countries = self.country.objects.all()
        updated_countries = []
        for country_in in countries_in:
            country_db = next((country for country in countries if country.code == country_in.code))
            country_db.languages.clear()
            for key, value in self.prepare_country_and_create_or_get_continent_and_currency(
                country_in, update=True
            ).items():
                setattr(country_db, key, value)
            updated_countries.append(country_db)
        self.country.objects.bulk_update(
            updated_countries,
            fields=[
                "name",
                "full_name",
                "capital",
                "continent",
                "population",
                "size",
                "code",
                "phone_code",
                "currency",
            ],
        )
        return self.set_languages_in_countries(countries_in, updated_countries)

    def query_continent_currency_filter(self):
        return self.country.objects.select_related("continent", "currency").prefetch_related(
            Prefetch("languages", to_attr="all_languages")
        )

    async def get_country_with_languages_by_name(self, name: str) -> Country | None:
        return (
            await self.query_continent_currency_filter()
            .filter(Q(name__iexact=name) | Q(full_name__iexact=name))
            .afirst()
        )

    async def get_country_with_languages_by_code(self, code: str) -> Country | None:
        return await self.query_continent_currency_filter().filter(code=code).afirst()


country_repository = CountryRepository()
