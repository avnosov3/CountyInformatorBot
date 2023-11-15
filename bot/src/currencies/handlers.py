from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext

from src.core.config import settings
from src.core.exceptions import NotFoundError
from src.currencies import text_before_buttons
from src.currencies.service import CurrencyService
from src.currencies.states import SearchCurrency
from src.currencies.texts import CURRENCY_INFO, CURRENCY_NOT_FOUND
from src.menu.buttons import come_back_to_main_menu, main_menu_buttons
from src.menu.callback_constants import FIND_CURRENCY

currency_router = Router(name=__name__)


@currency_router.callback_query(F.data == FIND_CURRENCY)
async def ask_currency_name(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer(text=text_before_buttons.INPUT_CURRENCY_NAME, reply_markup=come_back_to_main_menu())
    await state.set_state(SearchCurrency.name)
    await callback.answer()


@currency_router.message(SearchCurrency.name)
async def get_country(message: types.Message, state: FSMContext, currency_service: CurrencyService):
    currency_code = message.text.upper()
    USD = "USD"
    if currency_code == USD:
        await message.answer(
            text=CURRENCY_INFO.format(name=USD, exchange_rate=1), reply_markup=come_back_to_main_menu()
        )
        return
    try:
        currency_info = await currency_service.get_currency_by_name(currency_code)
        await message.answer(
            text=CURRENCY_INFO.format(**currency_info.model_dump()), reply_markup=come_back_to_main_menu()
        )
    except NotFoundError:
        await message.answer(text=CURRENCY_NOT_FOUND.format(name=currency_code), reply_markup=main_menu_buttons())
    except ConnectionError:
        await message.answer(text=settings.SERVICE_UNAVALIABLE, reply_markup=main_menu_buttons())
    await state.clear()
