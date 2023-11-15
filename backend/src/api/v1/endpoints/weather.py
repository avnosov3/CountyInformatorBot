from httpx._status_codes import code as status_code
from ninja import Router

from api.v1.endpoints import ErrorSchema, error_codes
from weather.schemas import WeatherSchema
from weather.services import weather_service

weather_router = Router()


@weather_router.get("/", response={status_code.OK: WeatherSchema, error_codes: ErrorSchema})
async def get_weather(request, latitude: float, longitude: float) -> WeatherSchema:
    return await weather_service.get_weather_by_coordinates(latitude, longitude)
