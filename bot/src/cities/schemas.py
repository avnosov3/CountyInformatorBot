from pydantic import BaseModel

from src.countries.schemas import CountryOutSchema


class StateOutSchema(BaseModel):
    name: str
    num_cities: int
    code: str


class CityOutSchema(BaseModel):
    name: str
    code: int
    population: int
    latitude: float
    longitude: float
    local_time: str
    utc: str
    country: CountryOutSchema
    state: StateOutSchema

    @classmethod
    def create_output(cls, data: dict) -> "CityOutSchema":
        country = data.pop("country")
        state = data.pop("state")
        return cls(country=CountryOutSchema.create_output(country), state=StateOutSchema(**state), **data)
