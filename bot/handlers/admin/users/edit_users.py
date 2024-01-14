from aiogram import Dispatcher, Bot
from aiogram.types import Message, CallbackQuery
from ....database.models.admin import Admin
from ....database.models.user import User
from ....keyboards.inline import start_kb
from ....keyboards.reply import user_param_kb
from ....keyboards.util import back_users_kb
from ....misc.util import _
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
import re


class EditUserFlow(StatesGroup):
    USER_ID_USERNAME = State()
    SELECTED_FIELD = State()
    NEW_VALUE = State()


async def start_edit_user(
    cq: CallbackQuery = None, msg: Message = None, state: FSMContext = None
):
    user_id = cq.from_user.id if cq else msg.from_user.id
    admin = Admin()
    language_db = admin.get_lang(user_id)

    text = _("user_edit_id_username", language_db)

    if cq:
        await cq.message.answer(text)
    elif msg:
        await msg.answer(text)

    if state:
        await EditUserFlow.USER_ID_USERNAME.set()
        await state.set_state(EditUserFlow.USER_ID_USERNAME.state)


async def process_user_id_username(msg: Message, state: FSMContext):
    user_id_username = msg.text
    await state.update_data(user_id_username=user_id_username)

    user_id = msg.from_user.id
    admin = Admin()
    language_db = admin.get_lang(user_id)

    user = User()
    user_data = user.get(user_id_username)

    if user_id_username == "/start":
        await state.finish()
        await msg.answer(_("start", language_db), reply_markup=start_kb(user_id))
    else:
        if user_data is None:
            text = f"{_('user_edit_unknown', language_db)}" f"{_('again', language_db)}"
            await msg.answer(text)
            return

        text = (
            f"{_('user_username', language_db)}  @{user_data['username']} ({user_data['user_id']})\n"
            f"{_('user_language', language_db)} - {user_data['language']}\n"
            f"{_('user_created', language_db)} - {user_data['created_at']}\n\n"
            f"{_('user_points', language_db)} - {user_data['points']}\n"
            f"{_('user_purchase_amount', language_db)} - {user_data['purchase_amount']}\n\n"
            f"{_('edit_field', language_db)}"
        )

        await msg.answer(text, reply_markup=user_param_kb(user_id_username))
        await EditUserFlow.SELECTED_FIELD.set()


async def process_field_selection(msg: Message, state: FSMContext):
    field = msg.text
    await state.update_data(selected_field=field)
    data = await state.get_data()
    user_id_username = data.get("user_id_username")

    user_id = msg.from_user.id
    admin = Admin()
    language_db = admin.get_lang(user_id)

    user = User()
    user_data = user.get(user_id_username)

    params = user_data.keys()
    if field not in params:
        text = f"{_('edit_params', language_db)}" f"{_('again', language_db)}"
        await msg.answer(text)
        return

    await msg.answer(_("edit_new", language_db))
    await EditUserFlow.NEW_VALUE.set()


async def process_new_value(msg: Message, state: FSMContext):
    user_id = msg.from_user.id
    admin = Admin()
    language_db = admin.get_lang(user_id)

    data = await state.get_data()
    user_id_username = data.get("user_id_username")
    selected_field = data.get("selected_field")

    new_value = msg.text
    if selected_field in ["purchase_amount", "order_amount"]:
        # Check if the input contains only numbers
        if not re.match("^[0-9]+$", new_value):
            await msg.answer(_("input_number", language_db))
            return
    await state.update_data(new_value=new_value)

    # Update the selected field in the database
    user = User()
    user.update(user_id_username, {selected_field: new_value})

    await msg.answer(
        _("user_edit_success", language_db), reply_markup=back_users_kb(user_id)
    )
    await state.finish()


def register_edit_users_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(
        start_edit_user, lambda c: c.data == "edit_user", state="*"
    )
    dp.register_message_handler(start_edit_user, commands=["edit_user"], state="*")
    dp.register_message_handler(
        process_user_id_username, state=EditUserFlow.USER_ID_USERNAME
    )
    dp.register_message_handler(
        process_field_selection, state=EditUserFlow.SELECTED_FIELD
    )
    dp.register_message_handler(process_new_value, state=EditUserFlow.NEW_VALUE)
