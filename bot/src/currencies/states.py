from aiogram.fsm.state import State, StatesGroup


class SearchCurrency(StatesGroup):
    name = State()
