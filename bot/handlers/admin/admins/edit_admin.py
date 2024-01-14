from aiogram import Dispatcher, Bot
from aiogram.types import Message, CallbackQuery
from ....database.models.admin import Admin
from ....database.models.user import User
from ....keyboards.inline import start_kb
from ....keyboards.reply import admin_param_kb
from ....keyboards.util import back_admins_kb
from ....misc.util import _
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
import re


class EditAdminFlow(StatesGroup):
    ADMIN_ID_USERNAME = State()
    SELECTED_FIELD = State()
    NEW_VALUE = State()


async def start_edit_admin(
    cq: CallbackQuery = None, msg: Message = None, state: FSMContext = None
):
    user_id = cq.from_user.id if cq else msg.from_user.id
    admin = Admin()
    language_db = admin.get_lang(user_id)

    text = _("admin_edit_id_username", language_db)

    if cq:
        await cq.message.answer(text)
    elif msg:
        await msg.answer(text)

    if state:
        await EditAdminFlow.ADMIN_ID_USERNAME.set()
        await state.set_state(EditAdminFlow.ADMIN_ID_USERNAME.state)


async def process_admin_id_username(msg: Message, state: FSMContext):
    admin_id_username = msg.text
    await state.update_data(admin_id_username=admin_id_username)

    user_id = msg.from_user.id
    admin = Admin()
    language_db = admin.get_lang(user_id)
    admin_data = admin.get(admin_id_username)

    if admin_id_username == "/start":
        await state.finish()
        await msg.answer(_("start", language_db), reply_markup=start_kb(user_id))
    else:
        if admin_data is None:
            text = (
                f"{_('admin_edit_unknown', language_db)}" f"{_('again', language_db)}"
            )
            await msg.answer(text)
            return

        text = (
            f"{_('user_username', language_db)}  @{admin_data['username']} (<code>{admin_data['user_id']}</code>)\n"
            f"{_('user_email', language_db)}  {admin_data['email']}\n"
            f"{_('user_language', language_db)} - {admin_data['language']}\n"
            f"{_('user_created', language_db)} - <i>{admin_data['created_at']}</i>\n\n"
            f"{_('edit_field', language_db)}"
        )

        await msg.answer(text, reply_markup=admin_param_kb(admin_id_username))
        await EditAdminFlow.SELECTED_FIELD.set()


async def process_field_selection(msg: Message, state: FSMContext):
    field = msg.text
    await state.update_data(selected_field=field)
    data = await state.get_data()
    admin_id_username = data.get("admin_id_username")

    user_id = msg.from_user.id
    admin = Admin()
    language_db = admin.get_lang(user_id)
    admin_data = admin.get(admin_id_username)

    params = admin_data.keys()
    if field not in params:
        text = f"{_('edit_params', language_db)}" f"{_('again', language_db)}"
        await msg.answer(text)
        return

    await msg.answer(_("edit_new", language_db))
    await EditAdminFlow.NEW_VALUE.set()


async def process_new_value(msg: Message, state: FSMContext):
    user_id = msg.from_user.id
    admin = Admin()
    language_db = admin.get_lang(user_id)

    data = await state.get_data()
    admin_id_username = data.get("admin_id_username")
    selected_field = data.get("selected_field")

    new_value = msg.text
    await state.update_data(new_value=new_value)

    # Update the selected field in the database
    admin.update(admin_id_username, {selected_field: new_value})

    await msg.answer(
        _("admin_edit_success", language_db), reply_markup=back_admins_kb(user_id)
    )
    await state.finish()


def register_edit_admin_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(
        start_edit_admin, lambda c: c.data == "edit_admin", state="*"
    )
    dp.register_message_handler(start_edit_admin, commands=["edit_admin"], state="*")
    dp.register_message_handler(
        process_admin_id_username, state=EditAdminFlow.ADMIN_ID_USERNAME
    )
    dp.register_message_handler(
        process_field_selection, state=EditAdminFlow.SELECTED_FIELD
    )
    dp.register_message_handler(process_new_value, state=EditAdminFlow.NEW_VALUE)
