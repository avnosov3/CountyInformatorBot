from aiogram import types

from src.menu.buttons import LIGHT_START_MENU_BUTTON
from src.menu.text_on_buttons import CITY_INFO, COUNTRY_INFO
from src.weather import callback_constants


def city_in_weather():
    buttons = [
        [types.InlineKeyboardButton(text=CITY_INFO, callback_data=callback_constants.FIND_CITY_IN_WEATHER)],
        LIGHT_START_MENU_BUTTON,
    ]
    return types.InlineKeyboardMarkup(inline_keyboard=buttons)


def get_country_info_in_weather():
    buttons = [
        [types.InlineKeyboardButton(text=COUNTRY_INFO, callback_data=callback_constants.FIND_CITY_IN_WEATHER)],
        LIGHT_START_MENU_BUTTON,
    ]
    return types.InlineKeyboardMarkup(inline_keyboard=buttons)
