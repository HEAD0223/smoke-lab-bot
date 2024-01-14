from aiogram import Dispatcher, Bot
from aiogram.types import Message, CallbackQuery
from ....database.models.admin import Admin
from ....database.models.manufacturer import Manufacturer
from ....keyboards.util import back_manufacturer_kb
from ....misc.util import _
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup


class AddManufacturerFlow(StatesGroup):
    MANUFACTURER_NAME = State()
    MANUFACTURER_COUNTRY = State()
    MANUFACTURER_DESCRIPTION = State()


async def start_add_manufacturer(
    cq: CallbackQuery = None, msg: Message = None, state: FSMContext = None
):
    user_id = cq.from_user.id if cq else msg.from_user.id
    admin = Admin()
    language_db = admin.get_lang(user_id)

    text = _("manufacturer_add_name", language_db)

    if cq:
        await cq.message.answer(text)
    elif msg:
        await msg.answer(text)

    if state:
        await AddManufacturerFlow.MANUFACTURER_NAME.set()
        await state.set_state(AddManufacturerFlow.MANUFACTURER_NAME.state)


async def process_manufacturer_name(msg: Message, state: FSMContext):
    manufacturer_name = msg.text
    await state.update_data(manufacturer_name=manufacturer_name)

    user_id = msg.from_user.id
    admin = Admin()
    language_db = admin.get_lang(user_id)

    await msg.answer(_("manufacturer_add_country", language_db))
    await AddManufacturerFlow.MANUFACTURER_COUNTRY.set()


async def process_manufacturer_country(msg: Message, state: FSMContext):
    manufacturer_country = msg.text
    await state.update_data(manufacturer_country=manufacturer_country)

    user_id = msg.from_user.id
    admin = Admin()
    language_db = admin.get_lang(user_id)

    await msg.answer(_("manufacturer_add_description", language_db))
    await AddManufacturerFlow.MANUFACTURER_DESCRIPTION.set()


async def process_manufacturer_description(msg: Message, state: FSMContext):
    user_id = msg.from_user.id
    admin = Admin()
    language_db = admin.get_lang(user_id)

    manufacturer_description = msg.text
    data = await state.get_data()
    manufacturer_name = data.get("manufacturer_name")
    manufacturer_country = data.get("manufacturer_country")

    # Perform the adding operation
    manufacturer = Manufacturer()
    manufacturer.create(
        manufacturer_name, manufacturer_country, manufacturer_description
    )

    # Clear the state
    await state.finish()
    await msg.answer(
        _("manufacturer_add_success", language_db),
        reply_markup=back_manufacturer_kb(user_id),
    )


def register_add_manufacturer_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(
        start_add_manufacturer, lambda c: c.data == "add_manufacturer", state="*"
    )
    dp.register_message_handler(
        start_add_manufacturer, commands=["add_manufacturer"], state="*"
    )
    dp.register_message_handler(
        process_manufacturer_name, state=AddManufacturerFlow.MANUFACTURER_NAME
    )
    dp.register_message_handler(
        process_manufacturer_country, state=AddManufacturerFlow.MANUFACTURER_COUNTRY
    )
    dp.register_message_handler(
        process_manufacturer_description,
        state=AddManufacturerFlow.MANUFACTURER_DESCRIPTION,
    )
