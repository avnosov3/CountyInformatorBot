from aiogram import types

from src.menu import callback_constants, text_on_buttons

LIGHT_START_MENU_BUTTON = [
    types.InlineKeyboardButton(
        text=text_on_buttons.COME_BACK_TO_MAIN_MENU, callback_data=callback_constants.COME_BACK_TO_MAIN_MENU
    )
]


def main_menu_buttons():
    buttons = [
        [types.InlineKeyboardButton(text=text_on_buttons.COUNTRY_INFO, callback_data=callback_constants.FIND_COUNTRY)],
        [
            types.InlineKeyboardButton(
                text=text_on_buttons.CITY_INFO,
                callback_data=callback_constants.FIND_CITY,
            )
        ],
        [
            types.InlineKeyboardButton(
                text=text_on_buttons.WEATHER_INFRO,
                callback_data=callback_constants.FIND_WEATHER,
            )
        ],
        [
            types.InlineKeyboardButton(
                text=text_on_buttons.CURRENCY_INFRO,
                callback_data=callback_constants.FIND_CURRENCY,
            )
        ],
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def come_back_to_main_menu():
    return types.InlineKeyboardMarkup(inline_keyboard=[LIGHT_START_MENU_BUTTON])
