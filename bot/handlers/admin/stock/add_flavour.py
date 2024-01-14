from aiogram import Dispatcher, Bot
from aiogram.types import Message, CallbackQuery, ContentTypes
from ....database.models.admin import Admin
from ....database.models.stock import Stock
from ....keyboards.util import back_stock_kb
from ....misc.util import _
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
import re
import base64
import io


class AddFlavourFlow(StatesGroup):
    CODE = State()
    FLAVOUR_NAME = State()
    AMOUNT = State()
    GRADIENT1 = State()
    GRADIENT2 = State()
    IMAGE_URL = State()


async def start_add(
    cq: CallbackQuery = None, msg: Message = None, state: FSMContext = None
):
    user_id = cq.from_user.id if cq else msg.from_user.id
    admin = Admin()
    language_db = admin.get_lang(user_id)

    text = _("stock_add_flavour_code", language_db)

    if cq:
        await cq.message.answer(text)
    elif msg:
        await msg.answer(text)

    if state:
        await AddFlavourFlow.CODE.set()
        await state.set_state(AddFlavourFlow.CODE.state)


async def process_code(msg: Message, state: FSMContext):
    user_id = msg.from_user.id
    admin = Admin()
    language_db = admin.get_lang(user_id)

    code = msg.text
    # Check if the input contains only numbers
    if not re.match("^[0-9]+$", code):
        await msg.answer(_("input_number", language_db))
        return

    stock = Stock()
    if stock.check(code):
        product = stock.get(code)

        if not product["flavours"]:
            text = _("flavours_empty", language_db)
        else:
            text = _("flavours_list", language_db)
            for flavour in product["flavours"]:
                text += f"👅 {flavour['flavour']} - x{flavour['amount']}\n"

        await state.update_data(code=code)
        await msg.answer(text)
        await msg.answer(_("stock_add_flavour_name", language_db))
        await AddFlavourFlow.FLAVOUR_NAME.set()
    else:
        return


async def process_flavour_name(msg: Message, state: FSMContext):
    flavour_name = msg.text
    await state.update_data(flavour_name=flavour_name)

    user_id = msg.from_user.id
    admin = Admin()
    language_db = admin.get_lang(user_id)

    await msg.answer(_("stock_add_amount", language_db))
    await AddFlavourFlow.AMOUNT.set()


async def process_amount(msg: Message, state: FSMContext):
    user_id = msg.from_user.id
    admin = Admin()
    language_db = admin.get_lang(user_id)

    amount = msg.text
    # Check if the input contains only numbers
    if not re.match("^[0-9]+$", amount):
        await msg.answer(_("input_number", language_db))
        return
    await state.update_data(amount=amount)

    await msg.answer(_("stock_add_flavour_gradient1", language_db))
    await AddFlavourFlow.GRADIENT1.set()


async def process_gradient1(msg: Message, state: FSMContext):
    user_id = msg.from_user.id
    admin = Admin()
    language_db = admin.get_lang(user_id)

    gradient1 = msg.text
    # Check if the input is in the format "#XXXXXX" where X is a hexadecimal character
    if not re.match(r"^#[0-9a-fA-F]{6}$", gradient1):
        await msg.answer(_("invalid_color_code", language_db))
        return
    await state.update_data(gradient1=gradient1)

    await msg.answer(_("stock_add_flavour_gradient2", language_db))
    await AddFlavourFlow.GRADIENT2.set()


async def process_gradient2(msg: Message, state: FSMContext):
    user_id = msg.from_user.id
    admin = Admin()
    language_db = admin.get_lang(user_id)

    gradient2 = msg.text
    # Check if the input is in the format "#XXXXXX" where X is a hexadecimal character
    if not re.match(r"^#[0-9a-fA-F]{6}$", gradient2):
        await msg.answer(_("invalid_color_code", language_db))
        return
    await state.update_data(gradient2=gradient2)

    await msg.answer(_("stock_add_url", language_db))
    await AddFlavourFlow.IMAGE_URL.set()


async def process_image_url(msg: Message, state: FSMContext):
    user_id = msg.from_user.id
    admin = Admin()
    language_db = admin.get_lang(user_id)

    # Check if the message contains an image
    if msg.photo:
        # Get the photo with the highest resolution (last item in the list)
        photo = msg.photo[-1]
        # Get the file_id of the photo
        file_id = photo.file_id
        # Use Bot.get_file() to get the file object
        bot = Bot.get_current()
        file = await bot.get_file(file_id)
        # Download the photo into a BytesIO object
        image_bytes = io.BytesIO()
        await file.download(destination_file=image_bytes)
        # Encode the image data to base64
        image_base64 = base64.b64encode(image_bytes.getvalue()).decode("utf-8")

        # Update the state with the image data
        await state.update_data(image_data=image_base64)

    stock = Stock()
    data = await state.get_data()
    code = data.get("code")
    flavour_name = data.get("flavour_name")
    amount = data.get("amount")
    gradient1 = data.get("gradient1")
    gradient2 = data.get("gradient2")
    image = data.get("image_data")

    existing_flavors = stock.get_flavors(code)
    new_flavor = {
        "flavour": flavour_name,
        "amount": amount,
        "gradient1": gradient1,
        "gradient2": gradient2,
        "image": image,
    }
    existing_flavors.append(new_flavor)

    stock.update(code, {"flavours": existing_flavors})

    # Clear the state
    await state.finish()
    await msg.answer(
        _("stock_add_flavour_success", language_db), reply_markup=back_stock_kb(user_id)
    )


def register_add_flavour_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(
        start_add, lambda c: c.data == "add_flavour", state="*"
    )
    dp.register_message_handler(start_add, commands=["add_flavour"], state="*")
    dp.register_message_handler(process_code, state=AddFlavourFlow.CODE)
    dp.register_message_handler(process_flavour_name, state=AddFlavourFlow.FLAVOUR_NAME)
    dp.register_message_handler(process_amount, state=AddFlavourFlow.AMOUNT)
    dp.register_message_handler(process_gradient1, state=AddFlavourFlow.GRADIENT1)
    dp.register_message_handler(process_gradient2, state=AddFlavourFlow.GRADIENT2)
    dp.register_message_handler(
        process_image_url,
        content_types=ContentTypes.PHOTO,
        state=AddFlavourFlow.IMAGE_URL,
    )
