from ninja import Field, Schema


class WeatherSchema(Schema):
    temperature: int = Field(..., alias="temp")
    feels_like: int
    humidity: int
    wind_speed: float
