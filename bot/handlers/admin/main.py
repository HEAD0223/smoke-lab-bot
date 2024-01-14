from aiogram import Dispatcher, Bot, types
from aiogram.types import Message, CallbackQuery
from ...database.models.admin import Admin
from ...database.models.user import User
from ...database.models.stock import Stock
from ...database.models.manufacturer import Manufacturer
from ...database.models.order import Order
from ...database.models.promo import Promo
from ...keyboards.inline import admin_kb
from ...keyboards.inline import stock_kb
from ...keyboards.inline import admins_kb
from ...keyboards.inline import users_kb
from ...keyboards.inline import manufacturer_kb
from ...keyboards.inline import orders_kb
from ...keyboards.util import back_admin_kb
from ...misc.util import _
from .stock.add_flavour import register_add_flavour_handlers
from .stock.remove_flavour import register_remove_flavour_handlers
from .stock.edit_flavour import register_edit_flavour_handlers
from .stock.add_stock import register_add_stock_handlers
from .stock.remove_stock import register_remove_stock_handlers
from .stock.edit_stock import register_edit_stock_handlers
from .admins.add_admin import register_add_admin_handlers
from .admins.remove_admin import register_remove_admin_handlers
from .admins.edit_admin import register_edit_admin_handlers
from .users.edit_users import register_edit_users_handlers
from .manufacturer.add_manufacturer import register_add_manufacturer_handlers
from .manufacturer.remove_manufacturer import register_remove_manufacturer_handlers
from .manufacturer.edit_manufacturer import register_edit_manufacturer_handlers
from .orders.find_order import register_find_order_handlers
from .orders.edit_order import register_edit_order_handlers
from .orders.remove_order import register_remove_order_handlers
import pandas as pd
import datetime
import io


async def admin(cq: CallbackQuery, bot: Bot):
    user_id = cq.from_user.id

    admin = Admin()
    language_db = admin.get_lang(user_id)

    await bot.edit_message_text(
        chat_id=user_id,
        text=_("admin", language_db),
        reply_markup=admin_kb(user_id),
        message_id=cq.message.message_id,
    )


async def stock(cq: CallbackQuery, bot: Bot):
    user_id = cq.from_user.id

    admin = Admin()
    language_db = admin.get_lang(user_id)
    stock = Stock()
    items = stock.get_stock()

    if not items:
        text = _("stock_empty", language_db)
    else:
        text = _("stock_list", language_db)
        for item in items:
            # Check if 'flavours' key exists and calculate the sum of 'amount' if available
            if "flavours" in item and isinstance(item["flavours"], list):
                total_amount = sum(int(flavor["amount"]) for flavor in item["flavours"])
            else:
                total_amount = 0

            text += f"📦 <code>{item['code']}</code> - <b>{item['name']}</b> - {item['price']} - <i>x{total_amount}</i>\n"

    await bot.edit_message_text(
        chat_id=user_id,
        text=text,
        reply_markup=stock_kb(user_id),
        message_id=cq.message.message_id,
    )


async def admins(cq: CallbackQuery, bot: Bot):
    user_id = cq.from_user.id

    admin = Admin()
    language_db = admin.get_lang(user_id)
    users = admin.get_admins()

    if not users:
        text = _("admin_empty", language_db)
    else:
        text = _("admin_list", language_db)
        for user in users:
            text += f"🗿 {user['username']} - <code>{user['user_id']}</code>\n"

    await bot.edit_message_text(
        chat_id=user_id,
        text=text,
        reply_markup=admins_kb(user_id),
        message_id=cq.message.message_id,
    )


async def users(cq: CallbackQuery, bot: Bot):
    user_id = cq.from_user.id

    admin = Admin()
    language_db = admin.get_lang(user_id)

    user = User()
    users_count = user.get_users_count()

    text = (
        f"{_('users_list', language_db)}"
        f"{_('users_amount', language_db)} - {users_count}\n"
    )

    await bot.edit_message_text(
        chat_id=user_id,
        text=text,
        reply_markup=users_kb(user_id),
        message_id=cq.message.message_id,
    )


async def manufacturer(cq: CallbackQuery, bot: Bot):
    user_id = cq.from_user.id

    admin = Admin()
    language_db = admin.get_lang(user_id)

    manufacturer = Manufacturer()
    manufacturers = manufacturer.get_manufacturers()

    if not manufacturers:
        text = _("manufacturer_empty", language_db)
    else:
        text = _("manufacturer_list", language_db)
        for manufacturer in manufacturers:
            text += f"🔨 {manufacturer['name']} - {manufacturer['country']}\n"

    await bot.edit_message_text(
        chat_id=user_id,
        text=text,
        reply_markup=manufacturer_kb(user_id),
        message_id=cq.message.message_id,
    )


async def orders(cq: CallbackQuery, bot: Bot):
    user_id = cq.from_user.id

    admin = Admin()
    language_db = admin.get_lang(user_id)
    order = Order()
    orders = order.get_orders()

    filtered_orders = [o for o in orders if o["user_id"] != 0]

    if not filtered_orders:
        text = _("orders_empty", language_db)
    else:
        text = _("orders_list", language_db)
        for order in filtered_orders:
            user_id_text = (
                f"(<code>{order['user_id']}</code>)" if order["user_id"] != 0 else ""
            )
            text += f"⏰  @{order['username']} {user_id_text}   -   {order['status']}\n"

    await bot.edit_message_text(
        chat_id=user_id,
        text=text,
        reply_markup=orders_kb(user_id),
        message_id=cq.message.message_id,
    )


async def promo(cq: CallbackQuery, bot: Bot):
    user_id = cq.from_user.id
    admin = Admin()
    language_db = admin.get_lang(user_id)

    promo = Promo()
    promo_data = promo.get_promos()
    filtered_promos = [
        promo_item for promo_item in promo_data if promo_item.get("usage", 0) == 0
    ]

    if not filtered_promos:
        text = _("promo_empty", language_db)
        await bot.edit_message_text(
            chat_id=user_id,
            text=text,
            reply_markup=back_admin_kb(user_id),
            message_id=cq.message.message_id,
        )
    else:
        text = f"{_('promo_show_done', language_db)}\n\n"

        for promo_item in filtered_promos:
            promo_user_id = promo_item.get("user_id", "")
            created_at = promo_item.get("created_at", "")
            if isinstance(created_at, datetime.datetime):
                created_at = created_at.strftime("%Y-%m-%d")
            promoName = promo_item.get("promoName", "")
            user = User()
            user_data = user.get(str(promo_user_id))

            text += f"    🎟️ @{user_data['username']} - <b>{promoName}</b> - <i>{created_at}</i>\n"

        await bot.edit_message_text(
            chat_id=user_id,
            text=text,
            reply_markup=back_admin_kb(user_id),
            message_id=cq.message.message_id,
        )


async def download_orders(cq: CallbackQuery, bot: Bot):
    user_id = cq.from_user.id

    admin = Admin()
    language_db = admin.get_lang(user_id)

    order = Order()
    all_orders_data = order.get_orders()
    orders_data = [
        order_data
        for order_data in all_orders_data
        if order_data.get("user_id", 0) == 0
    ]

    if not orders_data:
        text = _("orders_empty", language_db)
        await bot.answer_callback_query(cq.id, text)
    else:
        base_filename = "orders.xlsx"
        current_date = datetime.datetime.now().strftime("%Y-%m-%d")
        filename = f"{current_date}_{base_filename}"
        
        # Create a Pandas DataFrame from the filtered orders data
        orders_df = pd.DataFrame(orders_data)
        
        orders_df = pd.DataFrame(columns=[ "Date", "Product", "Flavor", "Quantity", "Price", "Total Price", "Earned (Month)"])
        
        for order in orders_data:
          if "cart" in order:
            for cart_item in order["cart"]:
               if "product" in cart_item:
                # Extract product information
                product = cart_item["product"]
                product_name = product.get("name", "")
                product_price = float(product.get("price", "0"))
                flavors_in_cart = cart_item.get("flavorsInCart", [])

                for flavor_item in flavors_in_cart:
                    flavour = flavor_item.get("flavour", "")
                    quantity = int(flavor_item.get("quantity", "0"))

                    # Calculate the total price for this flavor
                    total_price = product_price * quantity

                    # Append the data to the DataFrame
                    orders_df = orders_df.append(
                        {
                            "Date": order.get("created_at", ""),
                            "Product": product_name,
                            "Flavor": flavour,
                            "Quantity": quantity,
                            "Price": str(product_price),
                            "Total Price": total_price,
                        },
                        ignore_index=True,
                    )

        # Group by relevant columns and sum the quantity, price, and total_price
        grouped_orders_df = orders_df.groupby([pd.to_datetime(orders_df["Date"]).dt.strftime('%Y-%m'), "Product", "Flavor"]).agg(
          {"Quantity": "sum", "Price": "first", "Total Price": "sum"}
        ).reset_index()
        # Calculate the "Earned (Month)" column
        grouped_orders_df["Earned (Month)"] = (
          grouped_orders_df.groupby(["Date", "Product"])["Total Price"].transform("sum").round(2)
        )
        
        # Create an Excel file in memory
        excel_buffer = io.BytesIO()
        grouped_orders_df.to_excel(
            excel_buffer, index=False
        )  # You can customize this based on your data structure
        
        # Send the Excel file to the user
        excel_buffer.seek(0)
        document = types.InputFile(io.BytesIO(excel_buffer.getvalue()), filename=filename)
        await bot.send_document(chat_id=user_id, document=document)


def register_admin_handlers(dp: Dispatcher, bot: Bot):
    register_add_flavour_handlers(dp)
    register_remove_flavour_handlers(dp)
    register_edit_flavour_handlers(dp)
    register_add_stock_handlers(dp)
    register_remove_stock_handlers(dp)
    register_edit_stock_handlers(dp)
    register_add_admin_handlers(dp)
    register_remove_admin_handlers(dp)
    register_edit_admin_handlers(dp)
    register_edit_users_handlers(dp)
    register_add_manufacturer_handlers(dp)
    register_remove_manufacturer_handlers(dp)
    register_edit_manufacturer_handlers(dp)
    register_find_order_handlers(dp)
    register_edit_order_handlers(dp)
    register_remove_order_handlers(dp)
    dp.register_callback_query_handler(
        lambda cq: admin(cq, bot), lambda c: c.data in ["admin", "back_admin"]
    )
    dp.register_callback_query_handler(
        lambda cq: stock(cq, bot), lambda c: c.data in ["stock", "back_stock"]
    )
    dp.register_callback_query_handler(
        lambda cq: admins(cq, bot),
        lambda c: c.data in ["admins", "back_admins"],
    )
    dp.register_callback_query_handler(
        lambda cq: users(cq, bot),
        lambda c: c.data in ["users", "back_users"],
    )
    dp.register_callback_query_handler(
        lambda cq: manufacturer(cq, bot),
        lambda c: c.data in ["manufacturer", "back_manufacturer"],
    )
    dp.register_callback_query_handler(
        lambda cq: orders(cq, bot), lambda c: c.data in ["orders", "back_orders"]
    )
    dp.register_callback_query_handler(
        lambda cq: promo(cq, bot), lambda c: c.data in ["promo_admin"]
    )
    dp.register_callback_query_handler(
        lambda cq: download_orders(cq, bot), lambda c: c.data in ["download_orders"]
    )
