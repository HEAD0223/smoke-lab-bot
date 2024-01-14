from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from ..database.models.user import User
from ..database.models.admin import Admin
from ..database.main import admin_list
from ..misc.util import _


def back_kb(user_id):
    is_admin = user_id in admin_list or Admin().check(user_id, "user_id") is not None

    if is_admin:
        admin = Admin()
        language_db = admin.get_lang(user_id)
    else:
        user = User()
        language_db = user.get_lang(user_id)

    kb = InlineKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    back = InlineKeyboardButton(_("btn_back", language_db), callback_data="back")
    kb.add(back)

    return kb


def back_admin_kb(user_id):
    admin = Admin()
    language_db = admin.get_lang(user_id)

    kb = InlineKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    back = InlineKeyboardButton(_("btn_back", language_db), callback_data="back_admin")
    kb.add(back)

    return kb


def back_profile_kb(user_id):
    is_admin = user_id in admin_list or Admin().check(user_id, "user_id") is not None

    if is_admin:
        admin = Admin()
        language_db = admin.get_lang(user_id)
    else:
        user = User()
        language_db = user.get_lang(user_id)

    kb = InlineKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    back = InlineKeyboardButton(
        _("btn_back", language_db), callback_data="back_profile"
    )
    kb.add(back)

    return kb


def back_stock_kb(user_id):
    admin = Admin()
    language_db = admin.get_lang(user_id)

    kb = InlineKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    back = InlineKeyboardButton(_("btn_back", language_db), callback_data="back_stock")
    kb.add(back)

    return kb


def back_admins_kb(user_id):
    admin = Admin()
    language_db = admin.get_lang(user_id)

    kb = InlineKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    back = InlineKeyboardButton(_("btn_back", language_db), callback_data="back_admins")
    kb.add(back)

    return kb


def back_users_kb(user_id):
    admin = Admin()
    language_db = admin.get_lang(user_id)

    kb = InlineKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    back = InlineKeyboardButton(_("btn_back", language_db), callback_data="back_users")
    kb.add(back)

    return kb


def back_manufacturer_kb(user_id):
    admin = Admin()
    language_db = admin.get_lang(user_id)

    kb = InlineKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    back = InlineKeyboardButton(
        _("btn_back", language_db), callback_data="back_manufacturer"
    )
    kb.add(back)

    return kb


def back_order_kb(user_id):
    admin = Admin()
    language_db = admin.get_lang(user_id)

    kb = InlineKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    back = InlineKeyboardButton(_("btn_back", language_db), callback_data="back_orders")
    kb.add(back)

    return kb
