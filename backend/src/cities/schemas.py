import datetime

from ninja import Field, Schema

from cities.models import City
from countries.models import Country
from countries.schemas import CountryOutSchema, StateOutSchema


class BaseCitySchema(Schema):
    name: str
    code: int
    population: int
    latitude: float
    longitude: float


class CityInSchema(BaseCitySchema):
    code: int = Field(..., alias="id")
    country_code: str = Field(..., alias="countryCode")
    state_code: str = Field(..., alias="regionCode")


class CityOutSchema(BaseCitySchema):
    local_time: str
    utc: str
    country: CountryOutSchema
    state: StateOutSchema

    @classmethod
    def create(cls, city: City, country: Country, state: StateOutSchema) -> "CityOutSchema":
        utc = city.utc
        local_time = datetime.datetime.utcnow() + datetime.timedelta(hours=int(utc[:3]), minutes=int(utc[4:]))
        return cls(
            name=city.name,
            code=city.code,
            population=city.population,
            latitude=city.latitude,
            longitude=city.longitude,
            local_time=local_time.strftime("%h %d %H:%M"),
            utc=utc,
            country=CountryOutSchema.create(country),
            state=state,
        )
