from aiogram.fsm.state import State, StatesGroup


class SearchCity(StatesGroup):
    city_name = State()
    looking_region = State()
    looking_city = State()
    looking_weather_or_country_info = State()
