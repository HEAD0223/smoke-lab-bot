from aiogram import Dispatcher, Bot
from aiogram.types import Message, CallbackQuery, ContentTypes
from ....database.models.admin import Admin
from ....database.models.stock import Stock
from ....database.models.manufacturer import Manufacturer
from ....keyboards.util import back_stock_kb
from ....keyboards.reply import stock_manufacturer_param_kb
from ....keyboards.reply import volume_kb
from ....misc.util import _
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
import re
import random
import base64
import io


def generate_unique_code(stock):
    code_length = 6  # Set the desired length of the code
    code = generate_random_code(code_length)

    # Check if the code already exists
    while stock.check(code):
        code = generate_random_code(code_length)

    return code


def generate_random_code(length):
    digits = "0123456789"
    code = "".join(random.choices(digits, k=length))
    return code


class AddProductFlow(StatesGroup):
    PRODUCT_NAME = State()
    PRICE = State()
    VOLUME = State()
    DESCRIPTION = State()
    MANUFACTURER = State()
    IMAGE_URL = State()


async def start_add(
    cq: CallbackQuery = None, msg: Message = None, state: FSMContext = None
):
    user_id = cq.from_user.id if cq else msg.from_user.id
    admin = Admin()
    language_db = admin.get_lang(user_id)

    text = _("stock_add_name", language_db)

    if cq:
        await cq.message.answer(text)
    elif msg:
        await msg.answer(text)

    if state:
        await AddProductFlow.PRODUCT_NAME.set()
        await state.set_state(AddProductFlow.PRODUCT_NAME.state)


async def process_product_name(msg: Message, state: FSMContext):
    product_name = msg.text
    await state.update_data(product_name=product_name)

    user_id = msg.from_user.id
    admin = Admin()
    language_db = admin.get_lang(user_id)

    await msg.answer(_("stock_add_price", language_db))
    await AddProductFlow.PRICE.set()


async def process_price(msg: Message, state: FSMContext):
    user_id = msg.from_user.id
    admin = Admin()
    language_db = admin.get_lang(user_id)

    price = msg.text
    # Check if the input contains only numbers
    if not re.match("^[0-9]+$", price):
        await msg.answer(_("input_number", language_db))
        return
    await state.update_data(price=price)

    await msg.answer(_("stock_add_volume", language_db), reply_markup=volume_kb())
    await AddProductFlow.VOLUME.set()


async def process_volume(msg: Message, state: FSMContext):
    user_id = msg.from_user.id
    admin = Admin()
    language_db = admin.get_lang(user_id)

    volume = msg.text
    # Check if the input is 'None'
    if volume.lower() == "none":
        volume = "None"
    else:
        # Check if the input contains only numbers
        if not re.match("^[0-9]+$", volume):
            await msg.answer(_("input_number", language_db))
            return
    await state.update_data(volume=volume)

    await msg.answer(_("stock_add_description", language_db))
    await AddProductFlow.DESCRIPTION.set()


async def process_description(msg: Message, state: FSMContext):
    description = msg.text
    await state.update_data(description=description)

    user_id = msg.from_user.id
    admin = Admin()
    language_db = admin.get_lang(user_id)

    await msg.answer(
        _("stock_add_manufacturer", language_db),
        reply_markup=stock_manufacturer_param_kb(),
    )
    await AddProductFlow.MANUFACTURER.set()


async def process_manufacturer(msg: Message, state: FSMContext):
    user_id = msg.from_user.id
    admin = Admin()
    language_db = admin.get_lang(user_id)

    manufacturer_data = msg.text
    manufacturer = Manufacturer()
    manufacturers_db = manufacturer.get_manufacturers()

    manufacturer_names = [manufacturer.get("name") for manufacturer in manufacturers_db]

    if manufacturer_data not in manufacturer_names:
        text = f"{_('edit_params', language_db)}" f"{_('again', language_db)}"
        await msg.answer(text)
        return
    await state.update_data(manufacturer_data=manufacturer_data)

    await msg.answer(_("stock_add_url", language_db))
    await AddProductFlow.IMAGE_URL.set()


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

    # Get the collected data from the state
    data = await state.get_data()
    code = generate_unique_code(stock)
    product_name = data.get("product_name")
    price = data.get("price")
    description = data.get("description")
    manufacturer = data.get("manufacturer_data")
    image_data = data.get("image_data")
    volume = data.get("volume")

    stock.create(
        code, product_name, price, description, manufacturer, image_data, volume
    )

    # Clear the state
    await state.finish()
    await msg.answer(
        _("stock_add_success", language_db), reply_markup=back_stock_kb(user_id)
    )


def register_add_stock_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(start_add, lambda c: c.data == "add", state="*")
    dp.register_message_handler(start_add, commands=["add"], state="*")
    dp.register_message_handler(process_product_name, state=AddProductFlow.PRODUCT_NAME)
    dp.register_message_handler(process_price, state=AddProductFlow.PRICE)
    dp.register_message_handler(process_volume, state=AddProductFlow.VOLUME)
    dp.register_message_handler(process_description, state=AddProductFlow.DESCRIPTION)
    dp.register_message_handler(process_manufacturer, state=AddProductFlow.MANUFACTURER)
    dp.register_message_handler(
        process_image_url,
        content_types=ContentTypes.PHOTO,
        state=AddProductFlow.IMAGE_URL,
    )
