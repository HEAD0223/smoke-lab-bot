from aiogram import Dispatcher, Bot
from aiogram.types import Message, CallbackQuery, ContentTypes
from ....database.models.admin import Admin
from ....database.models.order import Order
from ....keyboards.inline import start_kb
from ....keyboards.util import back_order_kb
from ....misc.util import _
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
import re
import datetime


def generate_google_maps_link(address):
    # Replace spaces with '+' in the address for the Google Maps link
    formatted_address = address.replace(" ", "+")
    return f"https://www.google.com/maps/search/?api=1&query={formatted_address}"


class FindOrderFlow(StatesGroup):
    ORDER_ID = State()


async def start_find_order(
    cq: CallbackQuery = None, msg: Message = None, state: FSMContext = None
):
    user_id = cq.from_user.id if cq else msg.from_user.id
    admin = Admin()
    language_db = admin.get_lang(user_id)

    text = _("order_find_id", language_db)

    if cq:
        await cq.message.answer(text)
    elif msg:
        await msg.answer(text)

    if state:
        await FindOrderFlow.ORDER_ID.set()
        await state.set_state(FindOrderFlow.ORDER_ID.state)


async def process_order_id(msg: Message, state: FSMContext):
    order_id = msg.text
    await state.update_data(order_id=order_id)

    user_id = msg.from_user.id
    admin = Admin()
    language_db = admin.get_lang(user_id)

    if order_id == "/start":
        await state.finish()
        await msg.answer(_("start", language_db), reply_markup=start_kb(user_id))
    else:
        # Check if the input contains only numbers
        if not re.match("^[0-9]+$", order_id):
            await msg.answer(_("input_number", language_db))
            return

        order = Order()
        order_data = order.get(order_id)
        if order_data is None or order_id == "0":
            text = (
                f"{_('order_find_unknown', language_db)}" f"{_('again', language_db)}"
            )
            await msg.answer(text)
            return

        created_at = order_data.get("created_at", "")
        if isinstance(created_at, datetime.datetime):
            created_at = created_at.strftime("%Y-%m-%d")
        status = order_data.get("status", "")
        order_user_id = order_data.get("user_id", "")
        username = order_data.get("username", "")

        cart = order_data.get("cart", [])
        info = order_data.get("info", {})
        promo = info.get("promo", "")
        points = info.get("points", 0)
        name = info.get("name", "")
        phone = info.get("phone", "")
        address = info.get("address", "")
        comment = info.get("comment", "")

        address_link = generate_google_maps_link(address)
        cart_details = []
        total_price_of_all_flavors = 0
        total_quantity = 0

        for item in cart:
            product = item.get("product", {})
            product_name = product["name"]
            flavors_in_cart = item.get("flavorsInCart", [])
            total_price_for_item = 0
            total_quantity_for_item = sum(int(flavor["quantity"]) for flavor in flavors_in_cart)
            total_quantity += total_quantity_for_item

            flavor_details = "\n".join(
                f"  - {flavor['flavour']} x {flavor['quantity']} - ({int(flavor['quantity']) * int(product['price'])} MDL)"
                for flavor in flavors_in_cart
            )

            for flavor in flavors_in_cart:
                total_price_for_item += int(flavor["quantity"]) * int(product["price"])

            item_detail = f"🔶 {product_name}\n" + flavor_details

            cart_details.append(item_detail)
            total_price_of_all_flavors += total_price_for_item

        total_price_after_points = max(total_price_of_all_flavors - points, 0)
        cart_details_str = "\n\n".join(cart_details)

        additional_info = []
        if promo.strip():
            additional_info.append(f"{_('order_promo', language_db)} <i>{promo}</i>")

        if points != 0:
            additional_info.append(f"{_('order_points', language_db)} <i>{points}</i>")

        additional_info_str = "\n".join(additional_info)

        text = (
            f"@{username} (<code>{order_user_id}</code>)\n\n"
            + f"{_('order_show', language_db)}\n\n"
            + cart_details_str
            + (f"\n\n{additional_info_str}" if additional_info else "")
            + f"\n\n{_('order_price', language_db)} "
            + (f" <del>{total_price_of_all_flavors}</del>" if points != 0 else "")
            + f" <b>{total_price_after_points} MDL</b>"
            + (f"\n\n<b>{_('order_gift', language_db)}</b>" if total_quantity > 3 else "")
            + f"\n\n{_('order_created', language_db)} - <i>{created_at}</i>\n"
            + f"{_('order_status', language_db)} - <b>{status}</b>\n\n"
            + f"{_('user_name', language_db)} - {name}\n"
            + f"{_('user_phone', language_db)} - {phone}\n"
            + f"{_('user_address', language_db)} - <a href=\"{address_link}\">{address}</a>\n"
            + f"„{comment}“\n"
        )

        await state.finish()
        await msg.answer(text, reply_markup=back_order_kb(user_id))


def register_find_order_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(
        start_find_order, lambda c: c.data == "find_order", state="*"
    )
    dp.register_message_handler(start_find_order, commands=["find_order"], state="*")
    dp.register_message_handler(process_order_id, state=FindOrderFlow.ORDER_ID)
