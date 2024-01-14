from aiogram import Dispatcher, Bot
from aiogram.types import Message, CallbackQuery
from ....database.models.admin import Admin
from ....database.models.stock import Stock
from ....keyboards.reply import stock_flavour_kb
from ....keyboards.util import back_stock_kb
from ....keyboards.inline import start_kb
from ....misc.util import _
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
import re


class RemoveFlavourFlow(StatesGroup):
    CODE = State()
    SELECTED_FLAVOUR = State()


async def start_remove(
    cq: CallbackQuery = None, msg: Message = None, state: FSMContext = None
):
    user_id = cq.from_user.id if cq else msg.from_user.id
    admin = Admin()
    language_db = admin.get_lang(user_id)

    text = _("stock_remove_flavour_code", language_db)

    if cq:
        await cq.message.answer(text)
    elif msg:
        await msg.answer(text)

    if state:
        await RemoveFlavourFlow.CODE.set()
        await state.set_state(RemoveFlavourFlow.CODE.state)


async def process_code(msg: Message, state: FSMContext):
    code = msg.text

    user_id = msg.from_user.id
    admin = Admin()
    language_db = admin.get_lang(user_id)

    if code == "/start":
        await state.finish()
        await msg.answer(_("start", language_db), reply_markup=start_kb(user_id))
    else:
        # Check if the input contains only numbers
        if not re.match("^[0-9]+$", code):
            await msg.answer(_("input_number", language_db))
            return

        stock = Stock()
        if stock.check(code):
            product = stock.get(code)

            if not product["flavours"]:
                text = _("flavours_empty", language_db)
            else:
                text = _("flavours_list", language_db)
                for flavour in product["flavours"]:
                    text += f"👅 {flavour['flavour']} - x{flavour['amount']}\n"

            await state.update_data(code=code)
            await msg.answer(text)
            await msg.answer(
                _("stock_remove_selected_flavour", language_db),
                reply_markup=stock_flavour_kb(code),
            )
            await RemoveFlavourFlow.SELECTED_FLAVOUR.set()
        else:
            # Clear the state
            await state.finish()
            await msg.answer(
                _("stock_edit_unknown", language_db),
                reply_markup=back_stock_kb(user_id),
            )


async def process_selected_flavour(msg: Message, state: FSMContext):
    selected_flavour = msg.text

    user_id = msg.from_user.id
    admin = Admin()
    language_db = admin.get_lang(user_id)

    data = await state.get_data()
    code = data.get("code")
    stock = Stock()

    product = stock.get(code)
    if product and "flavours" in product and isinstance(product["flavours"], list):
        flavours = product["flavours"]

    # Find the index of the selected_flavour in the flavours list
    flavour_index = None
    for index, flavour_data in enumerate(flavours):
        if flavour_data.get("flavour") == selected_flavour:
            flavour_index = index
            break
    if flavour_index is not None:
        # Remove the selected_flavour from the flavours list
        deleted_flavour = flavours.pop(flavour_index)
        # Update the product in the database with the modified flavours
        stock.update(code, {"flavours": flavours})
        text = _("stock_remove_flavour_success", language_db)
    else:
        text = f"{_('edit_params', language_db)}" f"{_('again', language_db)}"
        await msg.answer(text)
        return

    # Clear the state
    await state.finish()
    await msg.answer(text, reply_markup=back_stock_kb(user_id))


def register_remove_flavour_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(
        start_remove, lambda c: c.data == "remove_flavour", state="*"
    )
    dp.register_message_handler(start_remove, commands=["remove_flavour"], state="*")
    dp.register_message_handler(process_code, state=RemoveFlavourFlow.CODE)
    dp.register_message_handler(
        process_selected_flavour, state=RemoveFlavourFlow.SELECTED_FLAVOUR
    )
