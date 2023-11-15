from aiogram import F, Router, filters, types
from aiogram.fsm.context import FSMContext

from src.cities import text_before_buttons
from src.cities.buttons import (
    country_info_or_come_back,
    get_countries,
    get_regions_on_buttons,
    weather_country_info_by_city,
    weather_info_or_come_back,
)
from src.cities.callback_constants import FIND_WEATHER
from src.cities.service import CityService
from src.cities.states import SearchCity
from src.cities.texts import CHOOSE_COUNTRY, CITY_INFO, CITY_NOT_FOUND
from src.core.config import settings
from src.core.exceptions import NotFoundError
from src.countries.texts import COUNTRY_INFO
from src.menu.buttons import come_back_to_main_menu, main_menu_buttons
from src.menu.callback_constants import FIND_CITY
from src.weather.service import WeatherService
from src.weather.texts import WEATHER_INFO

cities_router = Router(name=__name__)


@cities_router.callback_query(F.data == FIND_CITY)
async def ask_city_name(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer(text=text_before_buttons.INPUT_CITY_NAME, reply_markup=come_back_to_main_menu())
    await state.set_state(SearchCity.city_name)
    await callback.answer()


@cities_router.message(filters.StateFilter(SearchCity.city_name))
async def get_cities(message: types.Message, state: FSMContext, city_service: CityService):
    """
    Формируем список городов.
    Если название города принадлежит только одной стране, то сразу возвращаем информацию о городе.
    Если название города принадлежит нескольким странам, то уточняем у пользователя страну.
    """
    city_name = message.text.title()
    await state.update_data(city_name=city_name)
    try:
        cities = await city_service.get_cities_by_name(city_name)
        countries = set(city.country.name for city in cities)
    except NotFoundError:
        await message.answer(text=CITY_NOT_FOUND.format(name=city_name), reply_markup=main_menu_buttons())
        await state.clear()
        return
    except ConnectionError:
        await message.answer(text=settings.SERVICE_UNAVALIABLE, reply_markup=main_menu_buttons())
        await state.clear()
        return
    if len(countries) == settings.CITIES_AMOUNT:
        try:
            country_name = cities[0].country.name
            regions = set(await city_service.get_regions(city_name, country_name))
            if len(regions) == settings.CITIES_AMOUNT:
                city, *_ = await city_service.get_city_by_region(city_name=city_name, region=regions.pop())
                city_dump = city.model_dump()
                await message.answer(
                    text=CITY_INFO.format(
                        country_name=city.country.name,
                        state_name=city.state.name,
                        state_num_cities=city.state.num_cities,
                        **city_dump,
                    ),
                    reply_markup=weather_country_info_by_city(),
                )
                await state.update_data(**city_dump)
                await state.set_state(SearchCity.looking_weather_or_country_info)
            else:
                await message.answer(
                    text=text_before_buttons.CHOOSE_REGION.format(country_name=country_name, city_name=city_name),
                    reply_markup=get_regions_on_buttons(regions).as_markup(),
                )
                await state.set_state(SearchCity.looking_city)
        except ConnectionError:
            await message.answer(text=settings.SERVICE_UNAVALIABLE, reply_markup=main_menu_buttons())
            await state.clear()
    else:
        await message.answer(
            text=CHOOSE_COUNTRY.format(name=city_name), reply_markup=get_countries(countries).as_markup()
        )
        await state.set_state(SearchCity.looking_region)
        await state.update_data(city_name=city_name)


@cities_router.callback_query(filters.StateFilter(SearchCity.looking_region))
async def get_regions(callback: types.CallbackQuery, state: FSMContext, city_service: CityService):
    """
    После уточнения страны выдаём пользователю информацию о регионах в стране, где есть город.
    Если регион один, то выдаём информацию о городе.
    """
    data = await state.get_data()
    city_name = data["city_name"]
    try:
        regions = set(await city_service.get_regions(city_name, callback.data))
        if len(regions) == settings.CITIES_AMOUNT:
            city, *_ = await city_service.get_city_by_region(city_name=city_name, region=regions.pop())
            city_dump = city.model_dump()
            country_name = city.country.name
            await callback.message.answer(
                text=CITY_INFO.format(
                    country_name=country_name,
                    state_name=city.state.name,
                    state_num_cities=city.state.num_cities,
                    **city_dump,
                ),
                reply_markup=weather_country_info_by_city(),
            )
            await state.update_data(**city_dump)
            await state.set_state(SearchCity.looking_weather_or_country_info)
        else:
            await callback.message.answer(
                text=text_before_buttons.CHOOSE_REGION.format(country_name=callback.data, city_name=city_name),
                reply_markup=get_regions_on_buttons(regions).as_markup(),
            )
            await state.set_state(SearchCity.looking_city)
    except ConnectionError:
        await callback.message.answer(text=settings.SERVICE_UNAVALIABLE, reply_markup=main_menu_buttons())
        await state.clear()
    await callback.answer()


@cities_router.callback_query(filters.StateFilter(SearchCity.looking_city))
async def get_city(callback: types.CallbackQuery, state: FSMContext, city_service: CityService):
    """После уточнения региона выдаём пользователю информацию о стране."""
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
            reply_markup=weather_country_info_by_city(),
        )
        await state.update_data(**city_dump)
        await state.set_state(SearchCity.looking_weather_or_country_info)
    except ConnectionError:
        await callback.message.answer(text=settings.SERVICE_UNAVALIABLE, reply_markup=main_menu_buttons())
        await state.clear()
    await callback.answer()


@cities_router.callback_query(filters.StateFilter(SearchCity.looking_weather_or_country_info))
async def get_weather_or_country_info(
    callback: types.CallbackQuery, state: FSMContext, weather_service: WeatherService
):
    """Обрабатываем нажатие кнопок узнать погоду в городе и узнать информацию о стране."""
    city = await state.get_data()
    city_name = city["name"]
    callback_data = callback.data
    if callback_data == FIND_WEATHER:
        try:
            weather = await weather_service.get_weather(longitude=city["longitude"], latitude=city["latitude"])
            await callback.message.answer(
                text=WEATHER_INFO.format(
                    **weather.model_dump(),
                    name=city_name,
                    country_name=city["country"]["name"],
                    region_name=city["state"]["name"],
                ),
                reply_markup=country_info_or_come_back(),
            )
        except ConnectionError:
            await callback.message.answer(text=settings.SERVICE_UNAVALIABLE, reply_markup=main_menu_buttons())
            await state.clear()
    else:
        await callback.message.answer(
            text=COUNTRY_INFO.format(**city["country"]), reply_markup=weather_info_or_come_back()
        )
    await callback.answer()
