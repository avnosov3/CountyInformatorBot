from pydantic import BaseModel


class CountryOutSchema(BaseModel):
    name: str
    full_name: str
    capital: str
    continent: str
    population: int
    size: int
    code: str
    phone_code: str
    currency: str
    languages: str

    @classmethod
    def create_output(cls, data: dict) -> "CountryOutSchema":
        languages = data.pop("languages")
        return cls(languages=" ".join(languages), **data)
