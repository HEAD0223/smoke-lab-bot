from ..main import db


class Order:
    # order = Order()
    # order.create(user_id, username, created_at, items, status, comment)
    def create(
        self,
        user_id,
        username,
        created_at,
        items,
        status=None,
        comment=None,
    ):
        collection = db["orders"]
        order_exists = collection.find_one({"user_id": user_id})
        if order_exists:
            return None

        order_data = {
            "user_id": user_id,
            "username": username,
            "created_at": created_at,
            "items": items,
            "status": status,
            "comment": comment,
        }
        return collection.insert_one(order_data).inserted_id

    # order = Order()
    # order.update(user_id, {"status": "OK", "comment": "Text"})
    def update(self, user_id, updates):
        collection = db["orders"]
        update_data = {"$set": updates}
        result = collection.update_one({"user_id": int(user_id)}, update_data)
        return result.modified_count

    # order = Order()
    # order.check(user_id)
    def check(self, user_id):
        collection = db["orders"]
        order_data = collection.find_one({"user_id": int(user_id)})
        if order_data:
            return True
        return False

    # order = Order()
    # order.get(user_id)
    def get(self, user_id):
        collection = db["orders"]
        order_data = collection.find_one({"user_id": int(user_id)})
        return order_data

    # order = Order()
    # order.get_orders()
    def get_orders(self):
        collection = db["orders"]
        orders = collection.find()
        return [order for order in orders]

    # order = Order()
    # order.delete(user_id)
    def delete(self, user_id):
        collection = db["orders"]
        result = collection.delete_one({"user_id": int(user_id)})
        return result.deleted_count


def register_order_model(db):
    collection_names = db.list_collection_names()
    if "orders" not in collection_names:
        db.create_collection("orders")
