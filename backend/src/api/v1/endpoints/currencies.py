from httpx._status_codes import code as status_code
from ninja import Router

from api.v1.endpoints import ErrorSchema, error_codes
from currencies.schemas import CurrencyOutSchema
from currencies.service import currency_service

currency_router = Router()


@currency_router.get("/{currency_code}", response={status_code.OK: CurrencyOutSchema, error_codes: ErrorSchema})
async def get_currency_by_name(request, currency_code: str) -> CurrencyOutSchema:
    return await currency_service.get_exchange_rate(currency_code)
