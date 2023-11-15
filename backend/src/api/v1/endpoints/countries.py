from httpx._status_codes import code as status_code
from ninja import Router

from api.v1.endpoints import ErrorSchema, error_codes
from countries.schemas import CountryOutSchema
from countries.services import country_service

countries_router = Router()


@countries_router.get("/{name}", response={status_code.OK: CountryOutSchema, error_codes: ErrorSchema})
async def get_country_by_name(request, name: str) -> CountryOutSchema:
    return await country_service.get_country_by_name(name)
