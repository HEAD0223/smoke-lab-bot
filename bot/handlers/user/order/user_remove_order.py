from aiogram import Dispatcher, Bot
from aiogram.types import Message, CallbackQuery
from ....keyboards.util import back_profile_kb
from ....database.models.admin import Admin
from ....database.models.user import User
from ....database.models.order import Order
from ....database.models.stock import Stock
from ....database.models.promo import Promo
from ....database.main import admin_list
from ....misc.util import _


async def profile_order_remove(cq: CallbackQuery, bot: Bot):
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

    if order_data:
        order_status = order_data.get("status")

        if order_status == "✅":
            order.update(user_id, {"user_id": 0})

            cart = order_data.get("cart", [])
            info = order_data.get("info", {})
            promo_info = info.get("promo", "")
            points_info = info.get("points", 0)
            total_amount = 0

            for item in cart:
                product = item.get("product", {})
                total_price_for_item = 0

                flavors_in_cart = item.get("flavorsInCart", [])

                for flavor in flavors_in_cart:
                    total_price_for_item += int(flavor["quantity"]) * int(
                        product.get("price", 0)
                    )

                total_amount += total_price_for_item
            points_earned = int(total_amount * 0.1)

            user = User()
            user_id_str = str(user_id)
            user_data = user.get(user_id_str)
            user_points = user_data.get("points", 0)
            user_purchase_amount = user_data.get("purchase_amount", 0)

            # Update user points and purchase amount
            updated_user_points = max(user_points - points_info + points_earned, 0)
            user_purchase_amount += 1
            user.update(
                user_id,
                {
                    "points": updated_user_points,
                    "purchase_amount": user_purchase_amount,
                },
            )

            promo = Promo()
            promos_data = promo.get_promos()
            # Update the usage of the promo in promos
            for promo_entry in promos_data:
                if promo_entry["promoName"] == promo_info:
                    promo_usage = promo_entry["usage"]
                    promo_usage = max(promo_usage - 1, 0)
                    promo.update(promo_info, {"usage": promo_usage})

            text = (
                f"{_('order_points_earned', language_db)}  <b>{points_earned}</b>\n\n"
                + f"{_('order_remove_success', language_db)}\n"
            )
        else:
            cart = order_data.get("cart", [])
            flavor_quantities_to_return = {}

            for item in cart:
                product = item.get("product", {})
                product_code = product.get("code")
                flavors_in_cart = item.get("flavorsInCart", [])

                # Check if the product code is not in the flavor_quantities_to_return dictionary
                if product_code not in flavor_quantities_to_return:
                    flavor_quantities_to_return[product_code] = {}

                for flavor_in_cart in flavors_in_cart:
                    flavor_name = flavor_in_cart.get("flavour")
                    ordered_quantity = flavor_in_cart.get("quantity")

                    # Add the ordered quantity to the respective flavor in the dictionary
                    if flavor_name not in flavor_quantities_to_return[product_code]:
                        flavor_quantities_to_return[product_code][flavor_name] = 0
                    flavor_quantities_to_return[product_code][
                        flavor_name
                    ] += ordered_quantity

            for product_code, flavor_quantities in flavor_quantities_to_return.items():
                stock = Stock()  # Initialize the stock for this product
                product_in_stock = stock.get(product_code)

                if product_in_stock:
                    for flavor_name, quantity_to_return in flavor_quantities.items():
                        current_stock_flavors = product_in_stock.get("flavours", [])

                        # Find the flavor in the stock's flavors
                        for stock_flavor in current_stock_flavors:
                            if stock_flavor.get("flavour") == flavor_name:
                                current_flavor_amount = int(
                                    stock_flavor.get("amount", 0)
                                )
                                updated_flavor_amount = (
                                    current_flavor_amount + quantity_to_return
                                )

                                # Update the stock flavor with the new amount
                                stock_flavor["amount"] = str(updated_flavor_amount)

                    # Update the stock product with the updated flavors
                    stock.update(product_code, {"flavours": current_stock_flavors})

            order.delete(user_id)
            text = _("order_remove_success", language_db)
    else:
        text = _("order_remove_unknown", language_db)

    await bot.edit_message_text(
        chat_id=user_id,
        text=text,
        reply_markup=back_profile_kb(user_id),
        message_id=cq.message.message_id,
    )


def register_user_remove_order_handlers(dp: Dispatcher, bot: Bot):
    dp.register_callback_query_handler(
        lambda cq: profile_order_remove(cq, bot),
        lambda c: c.data == "profile_order_remove",
    )
