from aiogram import Dispatcher, Bot
from aiogram.types import Message, CallbackQuery
from ....database.models.admin import Admin
from ....database.models.manufacturer import Manufacturer
from ....keyboards.reply import stock_manufacturer_param_kb
from ....keyboards.util import back_manufacturer_kb
from ....misc.util import _
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
import re


class RemoveManufacturerFlow(StatesGroup):
    MANUFACTURER_NAME = State()


async def start_remove_manufacturer(
    cq: CallbackQuery = None, msg: Message = None, state: FSMContext = None
):
    user_id = cq.from_user.id if cq else msg.from_user.id
    admin = Admin()
    language_db = admin.get_lang(user_id)

    text = _("manufacturer_remove_name", language_db)

    if cq:
        await cq.message.answer(text, reply_markup=stock_manufacturer_param_kb())
    elif msg:
        await msg.answer(text, reply_markup=stock_manufacturer_param_kb())

    if state:
        await RemoveManufacturerFlow.MANUFACTURER_NAME.set()
        await state.set_state(RemoveManufacturerFlow.MANUFACTURER_NAME.state)


async def process_start_remove_manufacturer(msg: Message, state: FSMContext):
    manufacturer_name = msg.text

    user_id = msg.from_user.id
    admin = Admin()
    language_db = admin.get_lang(user_id)

    manufacturer = Manufacturer()

    # Perform the removal operation
    if manufacturer.get(manufacturer_name):
        manufacturer.delete(manufacturer_name)
        text = _("manufacturer_remove_success", language_db)
    else:
        text = _("manufacturer_remove_unknown", language_db)

    # Clear the state
    await state.finish()
    await msg.answer(text, reply_markup=back_manufacturer_kb(user_id))


def register_remove_manufacturer_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(
        start_remove_manufacturer, lambda c: c.data == "remove_manufacturer", state="*"
    )
    dp.register_message_handler(
        start_remove_manufacturer, commands=["remove_manufacturer"], state="*"
    )
    dp.register_message_handler(
        process_start_remove_manufacturer,
        state=RemoveManufacturerFlow.MANUFACTURER_NAME,
    )
