from aiogram import Dispatcher, Bot
from aiogram.types import Message, CallbackQuery
from ....database.models.admin import Admin
from ....keyboards.util import back_admins_kb
from ....misc.util import _
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
import datetime
import re


class AddAdminFlow(StatesGroup):
    ADMIN_USERNAME = State()
    ADMIN_ID = State()


async def start_add_admin(
    cq: CallbackQuery = None, msg: Message = None, state: FSMContext = None
):
    user_id = cq.from_user.id if cq else msg.from_user.id
    admin = Admin()
    language_db = admin.get_lang(user_id)

    text = _("admin_add_username", language_db)

    if cq:
        await cq.message.answer(text)
    elif msg:
        await msg.answer(text)

    if state:
        await AddAdminFlow.ADMIN_USERNAME.set()
        await state.set_state(AddAdminFlow.ADMIN_USERNAME.state)


async def process_admin_username(msg: Message, state: FSMContext):
    admin_username = msg.text
    await state.update_data(admin_username=admin_username)

    user_id = msg.from_user.id
    admin = Admin()
    language_db = admin.get_lang(user_id)

    await msg.answer(_("admin_add_id", language_db))
    await AddAdminFlow.ADMIN_ID.set()


async def process_admin_id(msg: Message, state: FSMContext):
    user_id = msg.from_user.id
    admin = Admin()
    language_db = admin.get_lang(user_id)

    admin_id = msg.text
    data = await state.get_data()
    admin_username = data.get("admin_username")

    # Check if the input contains only numbers
    if not re.match("^[0-9]+$", admin_id):
        await msg.answer(_("input_number", language_db))
        return

    # Perform the adding operation
    if not admin.get(admin_id):
        username = admin_username
        language = msg.from_user.language_code
        created_at = datetime.datetime.utcnow().date().isoformat()
        email = ""
        admin.create(
            admin_id,
            username,
            email,
            language,
            created_at,
        )

        text = _("admin_add_success", language_db)
    else:
        text = _("admin_add_unknown", language_db)

    # Clear the state
    await state.finish()
    await msg.answer(text, reply_markup=back_admins_kb(user_id))


def register_add_admin_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(
        start_add_admin, lambda c: c.data == "add_admin", state="*"
    )
    dp.register_message_handler(start_add_admin, commands=["add_admin"], state="*")
    dp.register_message_handler(
        process_admin_username, state=AddAdminFlow.ADMIN_USERNAME
    )
    dp.register_message_handler(process_admin_id, state=AddAdminFlow.ADMIN_ID)
