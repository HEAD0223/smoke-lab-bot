from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from ..database.models.stock import Stock
from ..database.models.user import User
from ..database.models.admin import Admin
from ..database.models.promo import Promo
from ..database.models.manufacturer import Manufacturer
from ..misc.util import _
from itertools import islice


def stock_param_kb(product_code):
    stock = Stock()
    item = stock.get(product_code)

    kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

    if item:
        params = item.keys()
        for param in islice(params, 1, None):
            # Exclude "flavours" from the parameters
            if param != "flavours":
                kb.add(KeyboardButton(param))

    return kb


def stock_flavour_kb(product_code):
    stock = Stock()
    item = stock.get(product_code)

    kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

    if item and "flavours" in item and isinstance(item["flavours"], list):
        flavours = item["flavours"]
        for flavour in flavours:
            kb.add(KeyboardButton(flavour["flavour"]))

    return kb


def stock_flavour_param_kb(product_code, selected_flavour):
    stock = Stock()
    item = stock.get(product_code)

    kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

    if item and "flavours" in item and isinstance(item["flavours"], list):
        flavours = item["flavours"]

        # Find the flavor with the matching name
        selected_flavour_info = None
        for flavour in flavours:
            if flavour["flavour"].strip() == selected_flavour.strip():
                selected_flavour_info = flavour
                break

        if selected_flavour_info:
            for param_name in selected_flavour_info:
                kb.add(KeyboardButton(param_name))

    return kb


def stock_manufacturer_param_kb():
    manufacturer = Manufacturer()
    manufacturers_data = manufacturer.get_manufacturers()

    kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

    if manufacturers_data:
        for manufacturer_data in manufacturers_data:
            name = manufacturer_data.get("name")
            kb.add(KeyboardButton(name))

    return kb


def user_param_kb(identifier):
    user = User()
    user_data = user.get(identifier)

    kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

    if user_data:
        params = user_data.keys()
        for param in islice(params, 2, None):
            kb.add(KeyboardButton(param))

    return kb


def admin_param_kb(identifier):
    admin = Admin()
    admin_data = admin.get(identifier)

    kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

    if admin_data:
        params = admin_data.keys()
        for param in islice(params, 2, None):
            kb.add(KeyboardButton(param))

    return kb


def manufacturer_param_kb(identifier):
    manufacturer = Manufacturer()
    manufacturer_data = manufacturer.get(identifier)

    kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

    if manufacturer_data:
        params = manufacturer_data.keys()
        for param in islice(params, 1, None):
            kb.add(KeyboardButton(param))

    return kb


def order_status_kb():
    status_type = ["⌛️", "📦", "✅"]

    kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

    for status in status_type:
        kb.add(KeyboardButton(status))

    return kb


def volume_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

    kb.add(KeyboardButton("None"))

    return kb


def promo_kb(user_id):
    promo = Promo()
    promo_list = promo.get(user_id)

    kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

    if promo_list:
        for promo_item in promo_list:
            promo_name = promo_item.get("promoName", "")
            kb.add(KeyboardButton(promo_name))

    return kb
