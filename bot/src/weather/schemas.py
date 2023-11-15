from pydantic import BaseModel


class WeatherOutSchema(BaseModel):
    temperature: int
    feels_like: int
    humidity: int
    wind_speed: float
