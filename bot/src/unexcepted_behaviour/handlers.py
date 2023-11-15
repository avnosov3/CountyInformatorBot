from aiogram import Router, types
from aiogram.fsm.context import FSMContext

from src.menu.buttons import main_menu_buttons

unexcepted_behavior = Router(name=__name__)

PLEASE_CHOOSE_BUTTONS = "Чтобы воспользоваться ботом, нажмите любую из этих кнопок:"


@unexcepted_behavior.message()
async def catch_unexcepted_behavior(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer(text=PLEASE_CHOOSE_BUTTONS, reply_markup=main_menu_buttons())
