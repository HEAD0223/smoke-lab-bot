from aiogram import Dispatcher, Bot
from aiogram.types import Message, CallbackQuery
from ....keyboards.inline import profile_order_kb
from ....keyboards.util import back_profile_kb
from ....database.models.admin import Admin
from ....database.models.user import User
from ....database.models.order import Order
from ....database.main import admin_list
from ....misc.util import _
import datetime


async def order(cq: CallbackQuery, bot: Bot):
    user_id = cq.from_user.id

    is_admin = user_id in admin_list or Admin().check(user_id, "user_id") is not None

    if is_admin:
        admin = Admin()
        language_db = admin.get_lang(user_id)
    else:
        user = User()
        language_db = user.get_lang(user_id)

    order = Order()
    order_data = order.get(user_id)

    if not order_data:
        text = _("order_none", language_db)
        await bot.edit_message_text(
            chat_id=user_id,
            text=text,
            reply_markup=back_profile_kb(user_id),
            message_id=cq.message.message_id,
        )
    else:
        created_at = order_data.get("created_at", "")
        if isinstance(created_at, datetime.datetime):
            created_at = created_at.strftime("%Y-%m-%d")
        status = order_data.get("status", "")

        cart = order_data.get("cart", [])
        info = order_data.get("info", {})
        promo = info.get("promo", "")
        points = info.get("points", 0)

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
            f"{_('order_show', language_db)}\n\n"
            + cart_details_str
            + (f"\n\n{additional_info_str}" if additional_info else "")
            + f"\n\n{_('order_price', language_db)} "
            + (f" <del>{total_price_of_all_flavors}</del>" if points != 0 else "")
            + f" <b>{total_price_after_points} MDL</b>"
            + (f"\n\n<b>{_('order_gift', language_db)}</b>" if total_quantity > 3 else "")
            + f"\n\n{_('order_created', language_db)} - <i>{created_at}</i>\n"
            + f"{_('order_status', language_db)} - <b>{status}</b>\n"
        )

        await bot.edit_message_text(
            chat_id=user_id,
            text=text,
            reply_markup=profile_order_kb(user_id),
            message_id=cq.message.message_id,
        )


def register_order_handlers(dp: Dispatcher, bot: Bot):
    dp.register_callback_query_handler(
        lambda cq: order(cq, bot), lambda c: c.data == "order"
    )
