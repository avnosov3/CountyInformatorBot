from pydantic import BaseModel, validator


class CurrencyOutSchema(BaseModel):
    name: str
    exchange_rate: float

    @validator("exchange_rate", pre=True, always=True)
    def round_float(cls, value):
        return round(value, 2)
