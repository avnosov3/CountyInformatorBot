from ninja import ModelSchema, Schema

from currencies.models import Currency


class CurrencyDBSchema(ModelSchema):
    class Config:
        model = Currency
        model_fields = [
            "code",
        ]


class CurrencyOutSchema(Schema):
    exchange_rate: float
