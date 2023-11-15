from aiogram import F, Router, filters, types
from aiogram.fsm.context import FSMContext

from src.cities.buttons import get_regions_on_buttons
from src.cities.service import CityService
from src.cities.text_before_buttons import CHOOSE_REGION, INPUT_CITY_NAME
from src.cities.texts import CITY_INFO, CITY_NOT_FOUND
from src.core.config import settings
from src.core.exceptions import NotFoundError
from src.countries import text_before_buttons
from src.countries.buttons import country_menu_buttons, weather_in_city
from src.countries.callback_constants import FIND_CITY_IN_COUNTRY, FIND_CURRENCY_IN_COUNTRY
from src.countries.service import CountryService
from src.countries.states import SearchCountry
from src.countries.texts import CITY_NOT_FOUND_IN_COUNTRY, COUNTRY_INFO, COUNTY_NOT_FOUND
from src.currencies.service import CurrencyService
from src.currencies.texts import CURRENCY_INFO
from src.menu.buttons import come_back_to_main_menu, main_menu_buttons
from src.menu.callback_constants import FIND_COUNTRY
from src.weather.service import WeatherService
from src.weather.texts import WEATHER_INFO

countries_router = Router(name=__name__)


@countries_router.callback_query(F.data == FIND_COUNTRY)
async def ask_country_name(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer(text=text_before_buttons.INPUT_COUNTRY_NAME, reply_markup=come_back_to_main_menu())
    await state.set_state(SearchCountry.name)
    await callback.answer()


@countries_router.message(SearchCountry.name)
async def get_country(message: types.Message, state: FSMContext, country_service: CountryService):
    country_name = message.text.title()
    await state.update_data(country_name=country_name)
    try:
        country = await country_service.get_country_by_name(country_name)
        await message.answer(text=COUNTRY_INFO.format(**country.model_dump()), reply_markup=country_menu_buttons())
        await state.update_data(currency=country.currency)
    except NotFoundError:
        await message.answer(text=COUNTY_NOT_FOUND.format(name=country_name), reply_markup=main_menu_buttons())
        await state.clear()
    except ConnectionError:
        await message.answer(text=settings.SERVICE_UNAVALIABLE, reply_markup=main_menu_buttons())
        await state.clear()


@countries_router.callback_query(F.data == FIND_CURRENCY_IN_COUNTRY)
async def get_currency_in_country(callback: types.CallbackQuery, state: FSMContext, currency_service: CurrencyService):
    data = await state.get_data()
    currency_code = data["currency"]
    USD = "USD"
    if currency_code == USD:
        await callback.message.answer(
            text=CURRENCY_INFO.format(name=USD, exchange_rate=1), reply_markup=come_back_to_main_menu()
        )
        await callback.answer()
        return
    try:
        currency_info = await currency_service.get_currency_by_name(currency_code)
        await callback.message.answer(
            text=CURRENCY_INFO.format(**currency_info.model_dump()), reply_markup=come_back_to_main_menu()
        )
    except ConnectionError:
        await callback.message.answer(text=settings.SERVICE_UNAVALIABLE, reply_markup=main_menu_buttons())
        await state.clear()
    await callback.answer()


@countries_router.callback_query(F.data == FIND_CITY_IN_COUNTRY)
async def ask_city_name(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer(text=INPUT_CITY_NAME, reply_markup=come_back_to_main_menu())
    await state.set_state(SearchCountry.input_city_name)
    await callback.answer()


@countries_router.message(filters.StateFilter(SearchCountry.input_city_name))
async def get_regions(message: types.Message, state: FSMContext, city_service: CityService):
    data = await state.get_data()
    city_name = message.text.title()
    await state.update_data(city_name=city_name)
    try:
        country_name = data["country_name"]
        regions = set(await city_service.get_regions(city_name=city_name, country=country_name))
        if len(regions) == 0:
            await message.answer(
                text=CITY_NOT_FOUND_IN_COUNTRY.format(name=city_name, country_name=data["country_name"]),
                reply_markup=come_back_to_main_menu(),
            )
        elif len(regions) == settings.CITIES_AMOUNT:
            try:
                city, *_ = await city_service.get_city_by_region(city_name=city_name, region=regions.pop())
                city_dump = city.model_dump()
                await message.answer(
                    text=CITY_INFO.format(
                        country_name=country_name,
                        state_name=city.state.name,
                        state_num_cities=city.state.num_cities,
                        **city_dump,
                    ),
                    reply_markup=weather_in_city(),
                )
                await state.update_data(**city_dump)
                await state.set_state(SearchCountry.find_weather_in_city)
            except ConnectionError:
                await message.answer(text=settings.SERVICE_UNAVALIABLE, reply_markup=main_menu_buttons())
                await state.clear()
        else:
            await message.answer(
                text=CHOOSE_REGION.format(country_name=country_name, city_name=city_name),
                reply_markup=get_regions_on_buttons(regions).as_markup(),
            )
            await state.set_state(SearchCountry.find_city)
    except NotFoundError:
        await message.answer(text=CITY_NOT_FOUND.format(name=city_name), reply_markup=come_back_to_main_menu())


@countries_router.callback_query(filters.StateFilter(SearchCountry.find_city))
async def get_city(callback: types.CallbackQuery, state: FSMContext, city_service: CityService):
    data = await state.get_data()
    city_name = data["city_name"]
    try:
        city, *_ = await city_service.get_city_by_region(city_name=city_name, region=callback.data)
        city_dump = city.model_dump()
        await callback.message.answer(
            text=CITY_INFO.format(
                country_name=city.country.name,
                state_name=city.state.name,
                state_num_cities=city.state.num_cities,
                **city_dump,
            ),
            reply_markup=weather_in_city(),
        )
        await state.update_data(**city_dump)
        await state.set_state(SearchCountry.find_weather_in_city)
    except NotFoundError:
        await callback.message.answer(text=CITY_NOT_FOUND.format(name=city_name), reply_markup=main_menu_buttons())
        await state.clear()
    except ConnectionError:
        await callback.message.answer(text=settings.SERVICE_UNAVALIABLE, reply_markup=main_menu_buttons())
        await state.clear()
    await callback.answer()


@countries_router.callback_query(filters.StateFilter(SearchCountry.find_weather_in_city))
async def find_weather_in_city(callback: types.CallbackQuery, state: FSMContext, weather_service: WeatherService):
    city = await state.get_data()
    try:
        weather = await weather_service.get_weather(longitude=city["longitude"], latitude=city["latitude"])
        await callback.message.answer(
            text=WEATHER_INFO.format(
                **weather.model_dump(),
                name=city["name"],
                country_name=city["country"]["name"],
                region_name=city["state"]["name"],
            ),
            reply_markup=come_back_to_main_menu(),
        )
    except ConnectionError:
        await callback.message.answer(text=settings.SERVICE_UNAVALIABLE, reply_markup=main_menu_buttons())
        await state.clear()
    await callback.answer()
