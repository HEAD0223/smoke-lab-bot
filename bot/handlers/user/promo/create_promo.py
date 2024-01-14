from aiogram import Dispatcher, Bot
from aiogram.types import Message, CallbackQuery
from ....database.models.admin import Admin
from ....database.models.user import User
from ....database.models.promo import Promo
from ....database.main import admin_list
from ....keyboards.util import back_profile_kb
from ....misc.util import _
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
import datetime


class CreatePromoFlow(StatesGroup):
    PROMO_NAME = State()


async def start_create(
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

    text = _("create_promo_name", language_db)

    if cq:
        await cq.message.answer(text)
    elif msg:
        await msg.answer(text)

    if state:
        await CreatePromoFlow.PROMO_NAME.set()
        await state.set_state(CreatePromoFlow.PROMO_NAME.state)


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
    usage = 10
    created_at = datetime.datetime.utcnow().date().isoformat()

    promo = Promo()
    promo.create(user_id, promoName, usage, created_at)

    # Clear the state
    await state.finish()
    await msg.answer(
        _("create_promo_success", language_db), reply_markup=back_profile_kb(user_id)
    )


def register_create_promo_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(
        start_create, lambda c: c.data == "profile_promo_create", state="*"
    )
    dp.register_message_handler(
        start_create, commands=["profile_promo_create"], state="*"
    )
    dp.register_message_handler(process_promo_name, state=CreatePromoFlow.PROMO_NAME)
