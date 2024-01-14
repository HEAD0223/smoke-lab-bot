from aiogram import Dispatcher, Bot
from aiogram.types import Message, CallbackQuery
from ...keyboards.util import back_kb
from ...keyboards.inline import profile_kb
from ...keyboards.inline import language_kb
from ...database.models.admin import Admin
from ...database.models.user import User
from ...database.main import admin_list
from ...misc.util import _
from .order.order import register_order_handlers
from .order.user_remove_order import register_user_remove_order_handlers
from .promo.promo import register_promo_handlers
from .promo.create_promo import register_create_promo_handlers
from .promo.delete_promo import register_delete_promo_handlers


async def profile(cq: CallbackQuery, bot: Bot):
    user_id = cq.from_user.id

    is_admin = user_id in admin_list or Admin().check(user_id, "user_id") is not None

    if is_admin:
        admin = Admin()
        language_db = admin.get_lang(user_id)
        user_id_str = str(user_id)
        user_data = admin.get(user_id_str)
        text = (
            f"{_('user_username', language_db)}  @{user_data['username']} (<code>{user_data['user_id']}</code>)\n"
            f"{_('user_email', language_db)}  {user_data['email']}\n"
            f"{_('user_created', language_db)} - <i>{user_data['created_at']}</i>\n"
        )
    else:
        user = User()
        language_db = user.get_lang(user_id)
        user_id_str = str(user_id)
        user_data = user.get(user_id_str)
        text = (
            f"{_('user_username', language_db)}  @{user_data['username']} (<code>{user_data['user_id']}</code>)\n\n"
            f"{_('user_points', language_db)} - <b>{user_data['points']}</b>\n"
            f"{_('user_purchase_amount', language_db)} - {user_data['purchase_amount']}\n\n"
            f"{_('user_created', language_db)} - <i>{user_data['created_at']}</i>\n"
        )

    await bot.edit_message_text(
        chat_id=user_id,
        text=text,
        reply_markup=profile_kb(user_id),
        message_id=cq.message.message_id,
    )


async def language(cq: CallbackQuery, bot: Bot):
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
        text=_("language", language_db),
        reply_markup=language_kb(user_id),
        message_id=cq.message.message_id,
    )


async def set_language(cq: CallbackQuery, bot: Bot):
    user_id = cq.from_user.id
    language = cq.data

    is_admin = user_id in admin_list or Admin().check(user_id, "user_id") is not None

    if is_admin:
        admin = Admin()
        admin.update(user_id, {"language": language})
    else:
        user = User()
        user.update(user_id, {"language": language})

    await bot.edit_message_text(
        chat_id=user_id,
        text=_("language", language),
        reply_markup=language_kb(user_id),
        message_id=cq.message.message_id,
    )


async def about(cq: CallbackQuery, bot: Bot):
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
        text=_("about", language_db),
        reply_markup=back_kb(user_id),
        message_id=cq.message.message_id,
    )


def register_user_handlers(dp: Dispatcher, bot: Bot):
    register_order_handlers(dp, bot)
    register_user_remove_order_handlers(dp, bot)
    register_promo_handlers(dp, bot)
    register_create_promo_handlers(dp)
    register_delete_promo_handlers(dp)
    dp.register_callback_query_handler(
        lambda cq: profile(cq, bot), lambda c: c.data in ["profile", "back_profile"]
    )
    dp.register_callback_query_handler(
        lambda cq: language(cq, bot), lambda c: c.data == "language"
    )
    dp.register_callback_query_handler(
        lambda cq: set_language(cq, bot), lambda c: c.data in ["en", "ru", "ro"]
    )
    dp.register_callback_query_handler(
        lambda cq: about(cq, bot), lambda c: c.data == "about"
    )
