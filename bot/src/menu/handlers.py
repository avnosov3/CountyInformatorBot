from aiogram import F, Router, types
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

from src.menu.buttons import main_menu_buttons
from src.menu.callback_constants import COME_BACK_TO_MAIN_MENU
from src.menu.text import SUCCESFUL_COME_BACK_TO_LIGHT_MENU, WELCOME_MESSAGE

menu_router = Router(name=__name__)


@menu_router.message(CommandStart())
async def start_menu(message: types.Message):
    await message.answer(text=WELCOME_MESSAGE, reply_markup=main_menu_buttons())


@menu_router.callback_query(F.data == COME_BACK_TO_MAIN_MENU)
async def light_menu(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.answer(text=SUCCESFUL_COME_BACK_TO_LIGHT_MENU, reply_markup=main_menu_buttons())
    await callback.answer()
