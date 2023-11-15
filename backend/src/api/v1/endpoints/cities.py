from httpx._status_codes import code as status_code
from ninja import Router

from api.v1.endpoints import ErrorSchema, error_codes
from cities.schemas import CityOutSchema
from cities.services import city_service

cities_router = Router()


@cities_router.get("/{name}", response={status_code.OK: list[CityOutSchema], error_codes: ErrorSchema})
async def get_cities_by_name(request, name: str) -> list[CityOutSchema]:
    return await city_service.get_cities_by_name(name)
