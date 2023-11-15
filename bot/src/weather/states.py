from aiogram.fsm.state import State, StatesGroup


class SearchWeather(StatesGroup):
    input_city_name = State()
    looking_region = State()
    looking_country = State()
    get_city_info = State()
    get_country_info = State()
