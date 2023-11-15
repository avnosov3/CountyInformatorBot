from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.cities import callback_constants, text_on_buttons
from src.menu.buttons import LIGHT_START_MENU_BUTTON


def get_countries(countries):
    keyboard = InlineKeyboardBuilder()

    for country in countries:
        keyboard.add(types.InlineKeyboardButton(text=country, callback_data=country))
    keyboard.add(
        *LIGHT_START_MENU_BUTTON,
    )
    return keyboard.adjust(1)


def get_regions_on_buttons(regions):
    keyboard = InlineKeyboardBuilder()
    for region in regions:
        keyboard.add(types.InlineKeyboardButton(text=region, callback_data=region))
    keyboard.add(
        *LIGHT_START_MENU_BUTTON,
    )
    return keyboard.adjust(1)


def weather_country_info_by_city():
    buttons = [
        [
            types.InlineKeyboardButton(
                text=text_on_buttons.FIND_WEATHER_IN_CITY, callback_data=callback_constants.FIND_WEATHER
            )
        ],
        [
            types.InlineKeyboardButton(
                text=text_on_buttons.FIND_COUNTRY_BY_CITY, callback_data=callback_constants.FIND_COUNTRY_BY_CITY
            )
        ],
        LIGHT_START_MENU_BUTTON,
    ]
    return types.InlineKeyboardMarkup(inline_keyboard=buttons)


def country_info_or_come_back():
    buttons = [
        [
            types.InlineKeyboardButton(
                text=text_on_buttons.FIND_COUNTRY_BY_CITY, callback_data=callback_constants.FIND_COUNTRY_BY_CITY
            )
        ],
        LIGHT_START_MENU_BUTTON,
    ]
    return types.InlineKeyboardMarkup(inline_keyboard=buttons)


def weather_info_or_come_back():
    buttons = [
        [
            types.InlineKeyboardButton(
                text=text_on_buttons.FIND_WEATHER_IN_CITY, callback_data=callback_constants.FIND_WEATHER
            )
        ],
        LIGHT_START_MENU_BUTTON,
    ]
    return types.InlineKeyboardMarkup(inline_keyboard=buttons)
