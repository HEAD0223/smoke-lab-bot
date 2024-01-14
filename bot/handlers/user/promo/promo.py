from aiogram import Dispatcher, Bot
from aiogram.types import Message, CallbackQuery
from ....keyboards.inline import profile_promo_kb
from ....database.models.admin import Admin
from ....database.models.user import User
from ....database.models.promo import Promo
from ....database.main import admin_list
from ....misc.util import _
import datetime


async def promo(cq: CallbackQuery, bot: Bot):
    user_id = cq.from_user.id

    is_admin = user_id in admin_list or Admin().check(user_id, "user_id") is not None

    if is_admin:
        admin = Admin()
        language_db = admin.get_lang(user_id)
    else:
        user = User()
        language_db = user.get_lang(user_id)

    promo = Promo()
    promo_data = promo.get(user_id)

    if not promo_data:
        text = _("promo_none", language_db)
        await bot.edit_message_text(
            chat_id=user_id,
            text=text,
            reply_markup=profile_promo_kb(user_id),
            message_id=cq.message.message_id,
        )
    else:
        text = f"{_('promo_show', language_db)}\n\n"

        for promo_item in promo_data:
            created_at = promo_item.get("created_at", "")
            if isinstance(created_at, datetime.datetime):
                created_at = created_at.strftime("%Y-%m-%d")
            promoName = promo_item.get("promoName", "")
            usage = promo_item.get("usage", "")

            text += f"    🎟️ {promoName} - <b>{usage}</b> - <i>{created_at}</i>\n"

        await bot.edit_message_text(
            chat_id=user_id,
            text=text,
            reply_markup=profile_promo_kb(user_id),
            message_id=cq.message.message_id,
        )


def register_promo_handlers(dp: Dispatcher, bot: Bot):
    dp.register_callback_query_handler(
        lambda cq: promo(cq, bot), lambda c: c.data == "promo"
    )
