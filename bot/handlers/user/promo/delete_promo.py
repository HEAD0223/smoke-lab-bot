from aiogram import Dispatcher, Bot
from aiogram.types import Message, CallbackQuery
from ....database.models.admin import Admin
from ....database.models.user import User
from ....database.models.promo import Promo
from ....database.main import admin_list
from ....keyboards.util import back_profile_kb
from ....keyboards.reply import promo_kb
from ....misc.util import _
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
import datetime


class DeletePromoFlow(StatesGroup):
    PROMO_NAME = State()


async def start_delete(
    cq: CallbackQuery = None, msg: Message = None, state: FSMContext = None
):
    user_id = cq.from_user.id if cq else msg.from_user.id
    is_admin = user_id in admin_list or Admin().check(user_id, "user_id") is not None

    if is_admin:
        admin = Admin()
        language_db = admin.get_lang(user_id)
    else:
        user = User()
        language_db = user.get_lang(user_id)

    text = _("delete_promo_name", language_db)

    if cq:
        await cq.message.answer(text, reply_markup=promo_kb(user_id))
    elif msg:
        await msg.answer(text, reply_markup=promo_kb(user_id))

    if state:
        await DeletePromoFlow.PROMO_NAME.set()
        await state.set_state(DeletePromoFlow.PROMO_NAME.state)


async def process_promo_name(msg: Message, state: FSMContext):
    promo_name = msg.text
    await state.update_data(promo_name=promo_name)

    user_id = msg.from_user.id
    is_admin = user_id in admin_list or Admin().check(user_id, "user_id") is not None

    if is_admin:
        admin = Admin()
        language_db = admin.get_lang(user_id)
    else:
        user = User()
        language_db = user.get_lang(user_id)

    data = await state.get_data()
    promoName = data.get("promo_name")

    promo = Promo()
    promo_list = promo.get(user_id)
    if promo_list:
        for promo_item in promo_list:
            existing_promo_name = promo_item.get("promoName", "")
            if promoName == existing_promo_name:
                promo.delete(promoName)
                await state.finish()
                await msg.answer(
                    _("delete_promo_success", language_db),
                    reply_markup=back_profile_kb(user_id),
                )
                return

    # Clear the state
    await state.finish()
    text = f"{_('edit_params', language_db)}" f"{_('again', language_db)}"
    await msg.answer(text, reply_markup=back_profile_kb(user_id))


def register_delete_promo_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(
        start_delete, lambda c: c.data == "profile_promo_delete", state="*"
    )
    dp.register_message_handler(
        start_delete, commands=["profile_promo_delete"], state="*"
    )
    dp.register_message_handler(process_promo_name, state=DeletePromoFlow.PROMO_NAME)
