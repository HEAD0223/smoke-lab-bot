from aiogram import Dispatcher, Bot
from aiogram.types import Message, CallbackQuery
from ..keyboards.inline import start_kb
from ..database.models.user import User
from ..database.models.admin import Admin
from ..database.main import admin_list
from ..misc.util import _
import datetime


async def start(msg: Message):
    user_id = msg.from_user.id
    username = msg.from_user.username if msg.from_user.username else None
    email = ""
    language = msg.from_user.language_code
    created_at = datetime.datetime.utcnow().date().isoformat()
    points = 0
    purchase_amount = 0

    is_admin = user_id in admin_list or Admin().check(user_id, "user_id") is not None

    if is_admin:
        admin = Admin()
        admin.create(
            user_id,
            username,
            email,
            language,
            created_at,
        )
        language_db = admin.get_lang(user_id)
    else:
        user = User()
        user.create(
            user_id,
            username,
            language,
            created_at,
            points,
            purchase_amount,
        )
        language_db = user.get_lang(user_id)

    await msg.answer(_("start", language_db), reply_markup=start_kb(user_id))


async def back(cq: CallbackQuery, bot: Bot):
    user_id = cq.from_user.id

    is_admin = user_id in admin_list or Admin().check(user_id, "user_id") is not None

    if is_admin:
        admin = Admin()
        language_db = admin.get_lang(user_id)
    else:
        user = User()
        language_db = user.get_lang(user_id)

    await bot.edit_message_text(
        chat_id=user_id,
        text=_("start", language_db),
        reply_markup=start_kb(user_id),
        message_id=cq.message.message_id,
    )


def register_other_handlers(dp: Dispatcher, bot: Bot) -> None:
    dp.register_message_handler(start, commands=["start"])
    dp.register_callback_query_handler(
        lambda cq: back(cq, bot), lambda c: c.data == "back"
    )
