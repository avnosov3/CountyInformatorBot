from aiogram.fsm.state import State, StatesGroup


class SearchCountry(StatesGroup):
    name = State()
    currency = State()
    find_city = State()
    input_city_name = State()
    find_weather_in_city = State()
