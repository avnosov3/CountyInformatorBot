from aiogram import types

from src.cities.text_on_buttons import FIND_WEATHER_IN_CITY
from src.countries import callback_constants, text_on_buttons
from src.menu.buttons import LIGHT_START_MENU_BUTTON


def country_menu_buttons():
    buttons = [
        [
            types.InlineKeyboardButton(
                text=text_on_buttons.FIND_CURRENCY_IN_COUNTRY, callback_data=callback_constants.FIND_CURRENCY_IN_COUNTRY
            )
        ],
        [
            types.InlineKeyboardButton(
                text=text_on_buttons.FIND_CITY_IN_COUNTRY, callback_data=callback_constants.FIND_CITY_IN_COUNTRY
            )
        ],
        LIGHT_START_MENU_BUTTON,
    ]
    return types.InlineKeyboardMarkup(inline_keyboard=buttons)


def weather_in_city():
    buttons = [
        [types.InlineKeyboardButton(text=FIND_WEATHER_IN_CITY, callback_data=callback_constants.FIND_WEATHER_IN_CITY)],
        LIGHT_START_MENU_BUTTON,
    ]
    return types.InlineKeyboardMarkup(inline_keyboard=buttons)
