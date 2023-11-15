from aiogram import F, Router, filters, types
from aiogram.fsm.context import FSMContext

from src.cities import text_before_buttons
from src.cities.buttons import get_countries, get_regions_on_buttons
from src.cities.service import CityService
from src.cities.texts import CHOOSE_COUNTRY, CITY_INFO, CITY_NOT_FOUND
from src.core.config import settings
from src.core.exceptions import NotFoundError
from src.countries.texts import COUNTRY_INFO
from src.menu.buttons import come_back_to_main_menu, main_menu_buttons
from src.menu.callback_constants import FIND_WEATHER
from src.weather.buttons import city_in_weather, get_country_info_in_weather
from src.weather.service import WeatherService
from src.weather.states import SearchWeather
from src.weather.texts import WEATHER_INFO, WEATHER_NOT_FOUND

weather_router = Router(name=__name__)


@weather_router.callback_query(F.data == FIND_WEATHER)
async def ask_city_name(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer(text=text_before_buttons.INPUT_CITY_NAME, reply_markup=come_back_to_main_menu())
    await state.set_state(SearchWeather.input_city_name)
    await callback.answer()


@weather_router.message(filters.StateFilter(SearchWeather.input_city_name))
async def input_city_name_and_get_countries(
    message: types.Message, state: FSMContext, city_service: CityService, weather_service: WeatherService
):
    """
    Формируем список городов.
    Если название города принадлежит только одной стране, то сразу возвращаем прогноз погоды в городе.
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
                await state.update_data(**city_dump)
                weather = await weather_service.get_weather(
                    longitude=city_dump["longitude"], latitude=city_dump["latitude"]
                )
                await message.answer(
                    text=WEATHER_INFO.format(
                        **weather.model_dump(),
                        name=city_name,
                        country_name=city.country.name,
                        region_name=city.state.name
                    ),
                    reply_markup=city_in_weather(),
                )
                await state.set_state(SearchWeather.get_city_info)
            else:
                await message.answer(
                    text=text_before_buttons.CHOOSE_REGION.format(country_name=country_name, city_name=city_name),
                    reply_markup=get_regions_on_buttons(regions).as_markup(),
                )
                await state.set_state(SearchWeather.looking_region)
        except ConnectionError:
            await message.answer(text=settings.SERVICE_UNAVALIABLE, reply_markup=main_menu_buttons())
            await state.clear()
    else:
        await message.answer(
            text=CHOOSE_COUNTRY.format(name=city_name), reply_markup=get_countries(countries).as_markup()
        )
        await state.set_state(SearchWeather.looking_country)
        await state.update_data(city_namename=city_name)


@weather_router.callback_query(filters.StateFilter(SearchWeather.looking_country))
async def get_regions(
    callback: types.CallbackQuery, state: FSMContext, city_service: CityService, weather_service: WeatherService
):
    """
    После уточнения страны выдаём пользователю информацию о регионах в стране, где есть город.
    Если регион один, то выдаём прогноз погоды в городе.
    """
    data = await state.get_data()
    city_name = data["city_name"]
    try:
        regions = set(await city_service.get_regions(city_name, callback.data))
        if len(regions) == settings.CITIES_AMOUNT:
            city, *_ = await city_service.get_city_by_region(city_name=city_name, region=regions.pop())
            city_dump = city.model_dump()
            await state.update_data(**city_dump)
            weather = await weather_service.get_weather(
                longitude=city_dump["longitude"], latitude=city_dump["latitude"]
            )
            await callback.message.answer(
                text=WEATHER_INFO.format(
                    **weather.model_dump(), name=city_name, country_name=city.country.name, region_name=city.state.name
                ),
                reply_markup=city_in_weather(),
            )
            await state.set_state(SearchWeather.get_city_info)
        else:
            await callback.message.answer(
                text=text_before_buttons.CHOOSE_REGION.format(country_name=callback.data, city_name=city_name),
                reply_markup=get_regions_on_buttons(regions).as_markup(),
            )
            await state.set_state(SearchWeather.looking_region)
    except ConnectionError:
        await callback.message.answer(text=settings.SERVICE_UNAVALIABLE, reply_markup=main_menu_buttons())
        await state.clear()
    await callback.answer()


@weather_router.callback_query(filters.StateFilter(SearchWeather.looking_region))
async def get_city(
    callback: types.CallbackQuery, state: FSMContext, city_service: CityService, weather_service: WeatherService
):
    data = await state.get_data()
    city_name = data["city_name"]
    try:
        city, *_ = await city_service.get_city_by_region(city_name=city_name, region=callback.data)
        city_dump = city.model_dump()
        await state.update_data(**city_dump)
        weather = await weather_service.get_weather(longitude=city_dump["longitude"], latitude=city_dump["latitude"])
        await callback.message.answer(
            text=WEATHER_INFO.format(
                **weather.model_dump(), name=city_name, country_name=city.country.name, region_name=city.state.name
            ),
            reply_markup=city_in_weather(),
        )
        await state.set_state(SearchWeather.get_city_info)
    except NotFoundError:
        await callback.message.answer(text=WEATHER_NOT_FOUND.format(name=city_name), reply_markup=main_menu_buttons())
        await state.clear()
    await callback.answer()


@weather_router.callback_query(filters.StateFilter(SearchWeather.get_city_info))
async def get_city_info(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await callback.message.answer(
        text=CITY_INFO.format(
            country_name=data["country"]["name"],
            state_name=data["state"]["name"],
            state_num_cities=data["state"]["num_cities"],
            **data
        ),
        reply_markup=get_country_info_in_weather(),
    )
    await state.set_state(SearchWeather.get_country_info)
    await callback.answer()


@weather_router.callback_query(filters.StateFilter(SearchWeather.get_country_info))
async def get_country_info(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await callback.message.answer(
        text=COUNTRY_INFO.format(**data["country"]),
        reply_markup=come_back_to_main_menu(),
    )
    await callback.answer()
