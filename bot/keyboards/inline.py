from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from ..database.models.user import User
from ..database.models.admin import Admin
from ..database.models.promo import Promo
from ..database.main import admin_list
from ..misc.util import _
from aiogram.types.web_app_info import WebAppInfo

webAppUrl = "https://smoke-lab.netlify.app/"


def start_kb(user_id):
    is_admin = user_id in admin_list or Admin().check(user_id, "user_id") is not None

    if is_admin:
        admin = Admin()
        language_db = admin.get_lang(user_id)
    else:
        user = User()
        language_db = user.get_lang(user_id)

    kb = InlineKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

    shop = InlineKeyboardButton(
        _("btn_web_app", language_db), web_app=WebAppInfo(url=webAppUrl)
    )
    profile = InlineKeyboardButton(
        _("btn_profile", language_db), callback_data="profile"
    )
    language = InlineKeyboardButton(
        _("btn_language", language_db), callback_data="language"
    )
    about = InlineKeyboardButton(_("btn_about", language_db), callback_data="about")
    admin = InlineKeyboardButton(_("btn_admin", language_db), callback_data="admin")
    if is_admin:
        kb.add(shop).add(profile).row(language, about).add(admin)
    else:
        kb.add(shop).add(profile).row(language, about)

    return kb


def profile_kb(user_id):
    is_admin = user_id in admin_list or Admin().check(user_id, "user_id") is not None

    if is_admin:
        admin = Admin()
        language_db = admin.get_lang(user_id)
    else:
        user = User()
        language_db = user.get_lang(user_id)

    kb = InlineKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

    order = InlineKeyboardButton(_("btn_order", language_db), callback_data="order")
    promo = InlineKeyboardButton(_("btn_promo", language_db), callback_data="promo")
    back = InlineKeyboardButton(_("btn_back", language_db), callback_data="back")
    kb.add(order).add(promo).add(back)

    return kb


def language_kb(user_id):
    is_admin = user_id in admin_list or Admin().check(user_id, "user_id") is not None

    if is_admin:
        admin = Admin()
        language_db = admin.get_lang(user_id)
    else:
        user = User()
        language_db = user.get_lang(user_id)

    kb = InlineKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

    english = InlineKeyboardButton(_("btn_us", language_db), callback_data="en")
    russian = InlineKeyboardButton(_("btn_ru", language_db), callback_data="ru")
    romanian = InlineKeyboardButton(_("btn_ro", language_db), callback_data="ro")
    back = InlineKeyboardButton(_("btn_back", language_db), callback_data="back")
    kb.add(english).row(russian, romanian).add(back)

    return kb


def admin_kb(user_id):
    admin = Admin()
    language_db = admin.get_lang(user_id)

    kb = InlineKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

    stock = InlineKeyboardButton(_("btn_stock", language_db), callback_data="stock")
    orders = InlineKeyboardButton(_("btn_orders", language_db), callback_data="orders")
    promo = InlineKeyboardButton(
        _("btn_promo", language_db), callback_data="promo_admin"
    )
    users = InlineKeyboardButton(_("btn_users", language_db), callback_data="users")
    admins = InlineKeyboardButton(_("btn_admins", language_db), callback_data="admins")
    download_orders = InlineKeyboardButton(
        _("btn_download", language_db), callback_data="download_orders"
    )
    back = InlineKeyboardButton(_("btn_back", language_db), callback_data="back")
    if user_id in admin_list:
        kb.add(stock).row(orders, promo).add(users).row(admins, download_orders).add(
            back
        )
    else:
        kb.add(stock).row(orders, promo).add(users).add(back)

    return kb


def stock_kb(user_id):
    admin = Admin()
    language_db = admin.get_lang(user_id)

    kb = InlineKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

    edit = InlineKeyboardButton(_("btn_edit", language_db), callback_data="edit")
    add = InlineKeyboardButton(_("btn_add", language_db), callback_data="add")
    remove = InlineKeyboardButton(_("btn_remove", language_db), callback_data="remove")
    manufacturer = InlineKeyboardButton(
        _("btn_manufacturer", language_db), callback_data="manufacturer"
    )
    edit_flavour = InlineKeyboardButton(
        _("btn_edit_flavour", language_db), callback_data="edit_flavour"
    )
    add_flavour = InlineKeyboardButton(
        _("btn_add_flavour", language_db), callback_data="add_flavour"
    )
    remove_flavour = InlineKeyboardButton(
        _("btn_remove_flavour", language_db), callback_data="remove_flavour"
    )
    back = InlineKeyboardButton(_("btn_back", language_db), callback_data="back_admin")
    kb.add(edit).row(add, remove).add(manufacturer).add(edit_flavour).row(
        add_flavour, remove_flavour
    ).add(back)

    return kb


def admins_kb(user_id):
    admin = Admin()
    language_db = admin.get_lang(user_id)

    kb = InlineKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

    edit = InlineKeyboardButton(_("btn_edit", language_db), callback_data="edit_admin")
    add = InlineKeyboardButton(_("btn_add", language_db), callback_data="add_admin")
    remove = InlineKeyboardButton(
        _("btn_remove", language_db), callback_data="remove_admin"
    )
    back = InlineKeyboardButton(_("btn_back", language_db), callback_data="back_admin")
    kb.add(edit).row(add, remove).add(back)

    return kb


def users_kb(user_id):
    admin = Admin()
    language_db = admin.get_lang(user_id)

    kb = InlineKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

    edit = InlineKeyboardButton(_("btn_edit", language_db), callback_data="edit_user")
    back = InlineKeyboardButton(_("btn_back", language_db), callback_data="back_admin")
    kb.add(edit).add(back)

    return kb


def manufacturer_kb(user_id):
    admin = Admin()
    language_db = admin.get_lang(user_id)

    kb = InlineKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

    edit = InlineKeyboardButton(
        _("btn_edit", language_db), callback_data="edit_manufacturer"
    )
    add = InlineKeyboardButton(
        _("btn_add", language_db), callback_data="add_manufacturer"
    )
    remove = InlineKeyboardButton(
        _("btn_remove", language_db), callback_data="remove_manufacturer"
    )
    back = InlineKeyboardButton(_("btn_back", language_db), callback_data="back_stock")
    kb.add(edit).row(add, remove).add(back)

    return kb


def orders_kb(user_id):
    admin = Admin()
    language_db = admin.get_lang(user_id)

    kb = InlineKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

    find = InlineKeyboardButton(_("btn_find", language_db), callback_data="find_order")
    edit = InlineKeyboardButton(_("btn_edit", language_db), callback_data="edit_order")
    remove = InlineKeyboardButton(
        _("btn_remove", language_db), callback_data="remove_order"
    )
    back = InlineKeyboardButton(_("btn_back", language_db), callback_data="back_admin")
    kb.add(find).row(edit, remove).add(back)

    return kb


def profile_order_kb(user_id):
    is_admin = user_id in admin_list or Admin().check(user_id, "user_id") is not None

    if is_admin:
        admin = Admin()
        language_db = admin.get_lang(user_id)
    else:
        user = User()
        language_db = user.get_lang(user_id)

    kb = InlineKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    remove = InlineKeyboardButton(
        _("btn_remove", language_db), callback_data="profile_order_remove"
    )
    back = InlineKeyboardButton(
        _("btn_back", language_db), callback_data="back_profile"
    )
    kb.add(remove).add(back)

    return kb


def profile_promo_kb(user_id):
    is_admin = user_id in admin_list or Admin().check(user_id, "user_id") is not None

    if is_admin:
        admin = Admin()
        language_db = admin.get_lang(user_id)
    else:
        user = User()
        language_db = user.get_lang(user_id)

    promo = Promo()
    promo_count = promo.count(user_id)

    kb = InlineKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    create = InlineKeyboardButton(
        _("btn_create", language_db), callback_data="profile_promo_create"
    )
    delete = InlineKeyboardButton(
        _("btn_delete", language_db), callback_data="profile_promo_delete"
    )
    back = InlineKeyboardButton(
        _("btn_back", language_db), callback_data="back_profile"
    )
    if promo_count > 2:
        kb.add(delete).add(back)
    elif promo_count == 0:
        kb.add(create).add(back)
    else:
        kb.add(create).add(delete).add(back)

    return kb
