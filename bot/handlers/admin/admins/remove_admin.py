from aiogram import Dispatcher, Bot
from aiogram.types import Message, CallbackQuery
from ....database.models.admin import Admin
from ....keyboards.util import back_admins_kb
from ....misc.util import _
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
import re


class RemoveAdminFlow(StatesGroup):
    ADMIN_ID = State()


async def start_remove_admin(
    cq: CallbackQuery = None, msg: Message = None, state: FSMContext = None
):
    user_id = cq.from_user.id if cq else msg.from_user.id
    admin = Admin()
    language_db = admin.get_lang(user_id)

    text = _("admin_remove_id", language_db)

    if cq:
        await cq.message.answer(text)
    elif msg:
        await msg.answer(text)

    if state:
        await RemoveAdminFlow.ADMIN_ID.set()
        await state.set_state(RemoveAdminFlow.ADMIN_ID.state)


async def process_start_remove_admin(msg: Message, state: FSMContext):
    admin_id = msg.text

    user_id = msg.from_user.id
    admin = Admin()
    language_db = admin.get_lang(user_id)

    # Check if the input contains only numbers
    if not re.match("^[0-9]+$", admin_id):
        await msg.answer(_("input_number", language_db))
        return

    # Perform the removal operation
    if admin.get(admin_id):
        admin.delete(admin_id)
        text = _("admin_remove_success", language_db)
    else:
        text = _("admin_remove_unknown", language_db)

    # Clear the state
    await state.finish()
    await msg.answer(text, reply_markup=back_admins_kb(user_id))


def register_remove_admin_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(
        start_remove_admin, lambda c: c.data == "remove_admin", state="*"
    )
    dp.register_message_handler(
        start_remove_admin, commands=["remove_admin"], state="*"
    )
    dp.register_message_handler(
        process_start_remove_admin, state=RemoveAdminFlow.ADMIN_ID
    )
