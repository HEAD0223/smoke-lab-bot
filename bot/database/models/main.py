from ..main import db
from ..models.user import register_user_model
from ..models.admin import register_admin_model
from ..models.stock import register_stock_model
from ..models.manufacturer import register_manufacturer_model
from ..models.order import register_order_model


def register_models() -> None:
    models = (
        register_user_model,
        register_admin_model,
        register_stock_model,
        register_manufacturer_model,
        register_order_model,
    )
    for model in models:
        model(db)
