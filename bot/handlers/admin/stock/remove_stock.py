from aiogram import Dispatcher, Bot
from aiogram.types import Message, CallbackQuery
from ....database.models.admin import Admin
from ....database.models.stock import Stock
from ....keyboards.util import back_stock_kb
from ....misc.util import _
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
import re


class RemoveProductFlow(StatesGroup):
    PRODUCT_CODE = State()


async def start_remove(
    cq: CallbackQuery = None, msg: Message = None, state: FSMContext = None
):
    user_id = cq.from_user.id if cq else msg.from_user.id
    admin = Admin()
    language_db = admin.get_lang(user_id)

    text = _("stock_remove_code", language_db)

    if cq:
        await cq.message.answer(text)
    elif msg:
        await msg.answer(text)

    if state:
        await RemoveProductFlow.PRODUCT_CODE.set()
        await state.set_state(RemoveProductFlow.PRODUCT_CODE.state)


async def process_product_code(msg: Message, state: FSMContext):
    product_code = msg.text

    user_id = msg.from_user.id
    admin = Admin()
    language_db = admin.get_lang(user_id)

    # Check if the input contains only numbers
    if not re.match("^[0-9]+$", product_code):
        await msg.answer(_("input_number", language_db))
        return

    # Perform the removal operation
    stock = Stock()
    if stock.check(product_code):
        stock.delete(product_code)
        text = _("stock_remove_success", language_db)
    else:
        text = _("stock_remove_unknown", language_db)

    # Clear the state
    await state.finish()
    await msg.answer(text, reply_markup=back_stock_kb(user_id))


def register_remove_stock_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(
        start_remove, lambda c: c.data == "remove", state="*"
    )
    dp.register_message_handler(start_remove, commands=["remove"], state="*")
    dp.register_message_handler(
        process_product_code, state=RemoveProductFlow.PRODUCT_CODE
    )
