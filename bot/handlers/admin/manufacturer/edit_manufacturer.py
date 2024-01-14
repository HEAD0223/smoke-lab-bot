from aiogram import Dispatcher, Bot
from aiogram.types import Message, CallbackQuery
from ....database.models.admin import Admin
from ....database.models.user import User
from ....database.models.manufacturer import Manufacturer
from ....keyboards.inline import start_kb
from ....keyboards.reply import manufacturer_param_kb
from ....keyboards.reply import stock_manufacturer_param_kb
from ....keyboards.util import back_manufacturer_kb
from ....misc.util import _
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup


class EditManufacturerFlow(StatesGroup):
    MANUFACTURER_NAME = State()
    SELECTED_FIELD = State()
    NEW_VALUE = State()


async def start_edit_manufacturer(
    cq: CallbackQuery = None, msg: Message = None, state: FSMContext = None
):
    user_id = cq.from_user.id if cq else msg.from_user.id
    admin = Admin()
    language_db = admin.get_lang(user_id)

    text = _("manufacturer_edit_name", language_db)

    if cq:
        await cq.message.answer(text, reply_markup=stock_manufacturer_param_kb())
    elif msg:
        await msg.answer(text, reply_markup=stock_manufacturer_param_kb())

    if state:
        await EditManufacturerFlow.MANUFACTURER_NAME.set()
        await state.set_state(EditManufacturerFlow.MANUFACTURER_NAME.state)


async def process_manufacturer_name(msg: Message, state: FSMContext):
    manufacturer_name = msg.text
    await state.update_data(manufacturer_name=manufacturer_name)

    user_id = msg.from_user.id
    admin = Admin()
    language_db = admin.get_lang(user_id)

    manufacturer = Manufacturer()
    manufacturer_data = manufacturer.get(manufacturer_name)

    if manufacturer_name == "/start":
        await state.finish()
        await msg.answer(_("start", language_db), reply_markup=start_kb(user_id))
    else:
        if manufacturer_data is None:
            text = (
                f"{_('manufacturer_edit_unknown', language_db)}"
                f"{_('again', language_db)}"
            )
            await msg.answer(text)
            return

        text = (
            f"{_('manufacturer_name', language_db)} - {manufacturer_data['name']}\n"
            f"{_('manufacturer_country', language_db)} - {manufacturer_data['country']}\n"
            f"{_('manufacturer_description', language_db)} - {manufacturer_data['description']}\n\n"
            f"{_('edit_field', language_db)}"
        )

        await msg.answer(text, reply_markup=manufacturer_param_kb(manufacturer_name))
        await EditManufacturerFlow.SELECTED_FIELD.set()


async def process_field_selection(msg: Message, state: FSMContext):
    field = msg.text
    await state.update_data(selected_field=field)
    data = await state.get_data()
    manufacturer_name = data.get("manufacturer_name")

    user_id = msg.from_user.id
    admin = Admin()
    language_db = admin.get_lang(user_id)

    manufacturer = Manufacturer()
    manufacturer_data = manufacturer.get(manufacturer_name)

    params = manufacturer_data.keys()
    if field not in params:
        text = f"{_('edit_params', language_db)}" f"{_('again', language_db)}"
        await msg.answer(text)
        return

    await msg.answer(_("edit_new", language_db))
    await EditManufacturerFlow.NEW_VALUE.set()


async def process_new_value(msg: Message, state: FSMContext):
    user_id = msg.from_user.id
    admin = Admin()
    language_db = admin.get_lang(user_id)

    data = await state.get_data()
    manufacturer_name = data.get("manufacturer_name")
    selected_field = data.get("selected_field")

    new_value = msg.text
    await state.update_data(new_value=new_value)

    # Update the selected field in the database
    manufacturer = Manufacturer()
    manufacturer.update(manufacturer_name, {selected_field: new_value})

    await msg.answer(
        _("manufacturer_edit_success", language_db),
        reply_markup=back_manufacturer_kb(user_id),
    )
    await state.finish()


def register_edit_manufacturer_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(
        start_edit_manufacturer, lambda c: c.data == "edit_manufacturer", state="*"
    )
    dp.register_message_handler(
        start_edit_manufacturer, commands=["edit_manufacturer"], state="*"
    )
    dp.register_message_handler(
        process_manufacturer_name, state=EditManufacturerFlow.MANUFACTURER_NAME
    )
    dp.register_message_handler(
        process_field_selection, state=EditManufacturerFlow.SELECTED_FIELD
    )
    dp.register_message_handler(process_new_value, state=EditManufacturerFlow.NEW_VALUE)
