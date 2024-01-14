from aiogram import Dispatcher, Bot
from aiogram.types import Message, CallbackQuery, ContentTypes
from ....database.models.admin import Admin
from ....database.models.stock import Stock
from ....database.models.manufacturer import Manufacturer
from ....keyboards.inline import start_kb
from ....keyboards.reply import stock_param_kb
from ....keyboards.reply import stock_flavour_kb
from ....keyboards.util import back_stock_kb
from ....keyboards.reply import stock_manufacturer_param_kb
from ....misc.util import _
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
import re
import base64
import io


class EditItemFlow(StatesGroup):
    PRODUCT_CODE = State()
    SELECTED_FIELD = State()
    NEW_IMAGE = State()
    NEW_VALUE = State()


async def start_edit_stock(
    cq: CallbackQuery = None, msg: Message = None, state: FSMContext = None
):
    user_id = cq.from_user.id if cq else msg.from_user.id
    admin = Admin()
    language_db = admin.get_lang(user_id)

    text = _("stock_edit_code", language_db)

    if cq:
        await cq.message.answer(text)
    elif msg:
        await msg.answer(text)

    if state:
        await EditItemFlow.PRODUCT_CODE.set()
        await state.set_state(EditItemFlow.PRODUCT_CODE.state)


async def process_product_code(msg: Message, state: FSMContext):
    product_code = msg.text
    await state.update_data(product_code=product_code)

    user_id = msg.from_user.id
    admin = Admin()
    language_db = admin.get_lang(user_id)

    stock = Stock()
    item = stock.get(product_code)

    if product_code == "/start":
        await state.finish()
        await msg.answer(_("start", language_db), reply_markup=start_kb(user_id))
    else:
        # Check if the input contains only numbers
        if not re.match("^[0-9]+$", product_code):
            await msg.answer(_("input_number", language_db))
            return
        if item is None:
            text = (
                f"{_('stock_edit_unknown', language_db)}" f"{_('again', language_db)}"
            )
            await msg.answer(text)
            return

        # Get the total amount from all flavors
        total_amount = sum(
            int(flavor.get("amount", 0)) for flavor in item.get("flavours", [])
        )
        # Decode the base64 image data back to bytes
        decode_image = base64.b64decode(item["image"])
        # Send the image back as a photo
        photo = io.BytesIO(decode_image)

        text = (
            f"{_('stock_name', language_db)} - {item['name']}\n"
            f"{_('stock_price', language_db)} - {item['price']}\n"
            f"{_('stock_code', language_db)} - {item['code']}\n"
            f"{_('stock_amount', language_db)} - {total_amount}\n"
            f"{_('stock_manufacturer', language_db)} - {item['manufacturer']}\n\n"
        )

        # Add flavors to the text
        text += f"{_('flavours_list', language_db)}:\n"
        for flavor in item.get("flavours", []):
            text += f"👅 {flavor['flavour']} - <i>x{flavor['amount']}</i>\n"

        text += f"\n{_('edit_field', language_db)}"

        await msg.delete()
        await msg.answer_photo(photo)
        await msg.answer(text, reply_markup=stock_param_kb(product_code))
        await EditItemFlow.SELECTED_FIELD.set()


async def process_field_selection(msg: Message, state: FSMContext):
    field = msg.text
    await state.update_data(selected_field=field)
    data = await state.get_data()
    product_code = data.get("product_code")

    user_id = msg.from_user.id
    admin = Admin()
    language_db = admin.get_lang(user_id)

    stock = Stock()
    item = stock.get(product_code)

    params = item.keys()
    if field not in params or field == "flavours":
        text = f"{_('edit_params', language_db)}" f"{_('again', language_db)}"
        await msg.answer(text)
        return

    if field == "manufacturer":
        await msg.answer(
            _("stock_add_manufacturer", language_db),
            reply_markup=stock_manufacturer_param_kb(),
        )
        await EditItemFlow.NEW_VALUE.set()
    elif field == "image":
        await msg.answer(_("stock_edit_new_url", language_db))
        await EditItemFlow.NEW_IMAGE.set()
    else:
        await msg.answer(_("edit_new", language_db))
        await EditItemFlow.NEW_VALUE.set()


async def process_new_image(msg: Message, state: FSMContext):
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
        await state.update_data(new_value=image_base64)

        data = await state.get_data()
        product_code = data.get("product_code")
        selected_field = data.get("selected_field")
        new_value = data.get("new_value")
        # Update the selected field in the database
        stock = Stock()
        stock.update(product_code, {selected_field: new_value})

        await msg.answer(
            _("stock_edit_success", language_db),
            reply_markup=back_stock_kb(),
        )
        await state.finish()


async def process_new_value(msg: Message, state: FSMContext):
    user_id = msg.from_user.id
    admin = Admin()
    language_db = admin.get_lang(user_id)

    data = await state.get_data()
    product_code = data.get("product_code")
    selected_field = data.get("selected_field")

    new_value = msg.text
    if selected_field == "manufacturer":
        # Get the list of manufacturer names
        manufacturer = Manufacturer()
        manufacturers_db = manufacturer.get_manufacturers()
        manufacturer_names = [
            manufacturer.get("name") for manufacturer in manufacturers_db
        ]
        # Check if the user's input is in the list of manufacturer names
        if new_value not in manufacturer_names:
            text = f"{_('edit_params', language_db)}" f"{_('again', language_db)}"
            await msg.answer(text)
            return
    elif selected_field in ["amount", "price", "code"]:
        # Check if the input contains only numbers
        if not re.match("^[0-9]+$", new_value):
            await msg.answer(_("input_number", language_db))
            return

    await state.update_data(new_value=new_value)

    # Update the selected field in the database
    stock = Stock()
    stock.update(product_code, {selected_field: new_value})

    await msg.answer(
        _("stock_edit_success", language_db), reply_markup=back_stock_kb(user_id)
    )
    await state.finish()


def register_edit_stock_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(
        start_edit_stock, lambda c: c.data == "edit", state="*"
    )
    dp.register_message_handler(start_edit_stock, commands=["edit"], state="*")
    dp.register_message_handler(process_product_code, state=EditItemFlow.PRODUCT_CODE)
    dp.register_message_handler(
        process_field_selection, state=EditItemFlow.SELECTED_FIELD
    )
    dp.register_message_handler(
        process_new_image,
        content_types=ContentTypes.PHOTO,
        state=EditItemFlow.NEW_IMAGE,
    )
    dp.register_message_handler(process_new_value, state=EditItemFlow.NEW_VALUE)
