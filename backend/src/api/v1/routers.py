import logging

from httpx._status_codes import code as status_code
from ninja import NinjaAPI

from api.v1.endpoints import ErrorSchema
from api.v1.endpoints.cities import cities_router
from api.v1.endpoints.countries import countries_router
from api.v1.endpoints.currencies import currency_router
from api.v1.endpoints.weather import weather_router
from core.exceptions import NotFoundError, StatusCodeNotOKError

logger = logging.getLogger(__name__)

api_v1 = NinjaAPI()


api_v1.add_router("/cities", cities_router, tags=["cities"])
api_v1.add_router("/countries", countries_router, tags=["countries"])
api_v1.add_router("/currencies", currency_router, tags=["currencies"])
api_v1.add_router("/weather", weather_router, tags=["weather"])


@api_v1.exception_handler(NotFoundError)
def not_found_error(request, exc):
    error_message, *_ = exc.args
    # return api_v1.create_response(request, dict(message=error_message), status=status_code.NOT_FOUND)
    return api_v1.create_response(request, ErrorSchema(message=error_message), status=status_code.NOT_FOUND)


@api_v1.exception_handler(ConnectionError)
def connection_error(request, exc):
    error_message, *_ = exc.args
    logger.exception(error_message)
    return api_v1.create_response(request, dict(message=error_message), status=status_code.SERVICE_UNAVAILABLE)


@api_v1.exception_handler(StatusCodeNotOKError)
def status_code_error(request, exc):
    error_message, *_ = exc.args
    logger.exception(error_message)
    return api_v1.create_response(request, dict(message=error_message), status=status_code.SERVICE_UNAVAILABLE)
