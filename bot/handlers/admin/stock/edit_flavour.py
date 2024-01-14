from aiogram import Dispatcher, Bot
from aiogram.types import Message, CallbackQuery, ContentTypes
from ....database.models.admin import Admin
from ....database.models.stock import Stock
from ....database.models.manufacturer import Manufacturer
from ....keyboards.inline import start_kb
from ....keyboards.reply import stock_flavour_kb
from ....keyboards.util import back_stock_kb
from ....keyboards.reply import stock_flavour_param_kb
from ....misc.util import _
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
import re
import base64
import io


class EditFlavourFlow(StatesGroup):
    PRODUCT_CODE = State()
    SELECTED_FLAVOUR = State()
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
        await EditFlavourFlow.PRODUCT_CODE.set()
        await state.set_state(EditFlavourFlow.PRODUCT_CODE.state)


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

        if not item["flavours"]:
            text = _("flavours_empty", language_db)
        else:
            text = _("flavours_list", language_db)
            for flavour in item["flavours"]:
                text += f"👅 {flavour['flavour']} - x{flavour['amount']}\n"

        text += f"\n{_('edit_field', language_db)}"

        await msg.delete()
        await msg.answer(text, reply_markup=stock_flavour_kb(product_code))
        await EditFlavourFlow.SELECTED_FLAVOUR.set()


async def process_selected_flavour(msg: Message, state: FSMContext):
    selected_flavour = msg.text
    await state.update_data(selected_flavour=selected_flavour)
    data = await state.get_data()
    product_code = data.get("product_code")

    user_id = msg.from_user.id
    admin = Admin()
    language_db = admin.get_lang(user_id)

    stock = Stock()
    product = stock.get(product_code)

    if product and "flavours" in product and isinstance(product["flavours"], list):
        flavours = product["flavours"]

    # Find the selected flavor
    selected_flavour_info = None
    for flavour in flavours:
        if selected_flavour.lower() in flavour["flavour"].lower():
            selected_flavour_info = flavour
            break

    if selected_flavour_info:
        # Decode the base64 image data back to bytes
        decode_image = base64.b64decode(selected_flavour_info.get("image", ""))
        # Send the image back as a photo
        photo = io.BytesIO(decode_image)

        # Extract the parameters for the selected flavor
        flavour = selected_flavour_info.get("flavour", "")
        gradient1 = selected_flavour_info.get("gradient1", "")
        gradient2 = selected_flavour_info.get("gradient2", "")
        amount = selected_flavour_info.get("amount", "")

        # You can construct the message text here
        text = f"{_('flavour', language_db)} - {flavour}\n"
        text += f"{_('amount', language_db)} {amount}\n"
        text += f"{_('gradient1', language_db)} {gradient1}\n"
        text += f"{_('gradient2', language_db)} {gradient2}\n\n"

        text += f'{_("edit_flavour_select", language_db)}'

        await msg.answer_photo(photo)
        await msg.answer(
            text,
            reply_markup=stock_flavour_param_kb(product_code, selected_flavour),
        )
        await EditFlavourFlow.SELECTED_FIELD.set()
    else:
        text = f"{_('edit_params', language_db)}" f"{_('again', language_db)}"
        await msg.answer(text)


async def process_selected_field(msg: Message, state: FSMContext):
    selected_field = msg.text
    await state.update_data(selected_field=selected_field)
    data = await state.get_data()
    product_code = data.get("product_code")

    user_id = msg.from_user.id
    admin = Admin()
    language_db = admin.get_lang(user_id)

    stock = Stock()
    product = stock.get(product_code)

    if product and "flavours" in product and isinstance(product["flavours"], list):
        flavours = product["flavours"]

    # Check if the selected field is in the flavor parameters
    field_in_flavour_params = any(
        selected_field.lower() in flavour.keys() for flavour in flavours
    )

    if not field_in_flavour_params:
        text = f"{_('edit_params', language_db)}" f"{_('again', language_db)}"
        await msg.answer(text)
        return

    if selected_field.lower() == "image":
        await msg.answer(_("stock_edit_new_url", language_db))
        await EditFlavourFlow.NEW_IMAGE.set()
    else:
        await msg.answer(_("edit_new", language_db))
        await EditFlavourFlow.NEW_VALUE.set()


async def process_new_image(msg: Message, state: FSMContext):
    user_id = msg.from_user.id
    admin = Admin()
    language_db = admin.get_lang(user_id)

    data = await state.get_data()
    product_code = data.get("product_code")
    selected_flavour = data.get("selected_flavour")

    stock = Stock()
    product = stock.get(product_code)

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

        # Update the selected flavor's image field in the database
        for flavour in product["flavours"]:
            if flavour["flavour"] == selected_flavour:
                flavour["image"] = image_base64
                break

        # Update the product data in the database
        stock.update(product_code, {"flavours": product["flavours"]})

        await msg.answer(
            _("stock_edit_success", language_db),
            reply_markup=back_stock_kb(user_id),
        )
        await state.finish()


async def process_new_value(msg: Message, state: FSMContext):
    user_id = msg.from_user.id
    admin = Admin()
    language_db = admin.get_lang(user_id)

    data = await state.get_data()
    product_code = data.get("product_code")
    selected_field = data.get("selected_field")
    selected_flavour = data.get("selected_flavour")

    new_value = msg.text
    if selected_field in ["gradient1", "gradient2"]:
        # Check if the input is in the format "#XXXXXX" where X is a hexadecimal character
        if not re.match(r"^#[0-9a-fA-F]{6}$", new_value):
            await msg.answer(_("invalid_color_code", language_db))
            return
    elif selected_field == "amount":
        # Check if the input contains only numbers
        if not re.match("^[0-9]+$", new_value):
            await msg.answer(_("input_number", language_db))
            return

    await state.update_data(new_value=new_value)

    # Update the selected flavour's field in the database
    stock = Stock()
    product = stock.get(product_code)

    for flavour in product["flavours"]:
        if flavour["flavour"] == selected_flavour:
            flavour[selected_field] = new_value
            break

    # Update the product data in the database with the modified flavour
    stock.update(product_code, {"flavours": product["flavours"]})

    await msg.answer(
        _("stock_edit_success", language_db), reply_markup=back_stock_kb(user_id)
    )
    await state.finish()


def register_edit_flavour_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(
        start_edit_stock, lambda c: c.data == "edit_flavour", state="*"
    )
    dp.register_message_handler(start_edit_stock, commands=["edit_flavour"], state="*")
    dp.register_message_handler(
        process_product_code, state=EditFlavourFlow.PRODUCT_CODE
    )
    dp.register_message_handler(
        process_selected_flavour, state=EditFlavourFlow.SELECTED_FLAVOUR
    )
    dp.register_message_handler(
        process_selected_field, state=EditFlavourFlow.SELECTED_FIELD
    )
    dp.register_message_handler(
        process_new_image,
        content_types=ContentTypes.PHOTO,
        state=EditFlavourFlow.NEW_IMAGE,
    )
    dp.register_message_handler(process_new_value, state=EditFlavourFlow.NEW_VALUE)
