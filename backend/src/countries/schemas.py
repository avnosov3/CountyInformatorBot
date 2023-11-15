from ninja import Field, ModelSchema, Schema

from countries.models import Continent, Country, Language


class CountryInSchema(Schema):
    name: str | None
    full_name: str | None
    capital: str | None
    continent: str | None
    population: int | None
    size: int | None
    code: str
    phone_code: str | None
    currency: str | None
    languages: list[str]

    @classmethod
    def parse(cls, country_in: dict) -> "CountryInSchema":
        name_key = country_in.get("name")
        capital = country_in.get("capital")
        continent = country_in.get("continents")
        currency = country_in.get("currencies")
        phone_code_key = country_in.get("idd")
        languages = country_in.get("languages")
        return cls(
            name=name_key.get("common") if name_key else None,
            full_name=name_key.get("official") if name_key else None,
            capital=capital[0] if capital else None,
            continent=continent[0] if continent else None,
            population=country_in.get("population"),
            size=country_in.get("area"),
            code=country_in.get("cca2"),
            currency=list(currency.keys())[0] if currency else None,
            phone_code=phone_code_key.get("root") if phone_code_key else None,
            languages=list(languages.values()),
        )


class LanguageDBSchema(ModelSchema):
    class Config:
        model = Language
        model_fields = [
            "name",
        ]


class ContinentDBSchema(ModelSchema):
    class Config:
        model = Continent
        model_fields = [
            "name",
        ]


class CountryOutSchema(CountryInSchema):
    @classmethod
    def create(cls, country: Country) -> "CountryOutSchema":
        all_languages = country.all_languages
        return cls(
            name=country.name,
            full_name=country.full_name,
            capital=country.capital,
            continent=country.continent.name,
            population=country.population,
            size=country.size,
            code=country.code,
            currency=country.currency.code,
            phone_code=country.phone_code,
            languages=[language.name for language in all_languages],
        )


class StateInSchema(Schema):
    name: str
    num_cities: int = Field(..., alias="numCities")
    code: str = Field(..., alias="isoCode")


class StateOutSchema(Schema):
    name: str
    num_cities: int
    code: str
