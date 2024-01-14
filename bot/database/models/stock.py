from ..main import db


class Stock:
    # stock = Stock()
    # stock.create(code, name, price, description, manufacturer, image, volume, flavours)
    def create(
        self,
        code,
        name,
        price,
        description,
        manufacturer,
        image,
        volume=None,
        flavours=None,
    ):
        collection = db["stock"]
        item_exists = collection.find_one({"code": code})
        if item_exists:
            return None

        item_data = {
            "code": code,
            "name": name,
            "price": price,
            "description": description,
            "manufacturer": manufacturer,
            "image": image,
            "volume": volume,
            "flavours": flavours or [],
        }
        return collection.insert_one(item_data).inserted_id

    # stock = Stock()
    # stock.update(code, {"name": "Product Name", "amount": "23"})
    def update(self, code, updates):
        collection = db["stock"]
        update_data = {"$set": updates}
        result = collection.update_one({"code": code}, update_data)
        return result.modified_count

    # stock = Stock()
    # stock.check(code)
    def check(self, code):
        collection = db["stock"]
        item_data = collection.find_one({"code": code})
        if item_data:
            return True
        return False

    # stock = Stock()
    # stock.get(code)
    def get(self, code):
        collection = db["stock"]
        item_data = collection.find_one({"code": code})
        return item_data

    # stock = Stock()
    # stock.get_stock()
    def get_stock(self):
        collection = db["stock"]
        items = collection.find()
        return [item for item in items]

    # stock = Stock()
    # stock.get_flavors(code)
    def get_flavors(self, code):
        collection = db["stock"]
        item = collection.find_one({"code": code})
        if item:
            return item.get("flavours", [])
        else:
            return []

    # stock = Stock()
    # stock.delete(code)
    def delete(self, code):
        collection = db["stock"]
        result = collection.delete_one({"code": code})
        return result.deleted_count


def register_stock_model(db):
    collection_names = db.list_collection_names()
    if "stock" not in collection_names:
        db.create_collection("stock")
