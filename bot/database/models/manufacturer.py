from ..main import db


class Manufacturer:
    # manufacturer = Manufacturer()
    # manufacturer.create(name, country, description)
    def create(
        self,
        name,
        country,
        description,
    ):
        collection = db["manufacturer"]
        item_exists = collection.find_one({"name": name})
        if item_exists:
            return None

        item_data = {
            "name": name,
            "country": country,
            "description": description,
        }
        return collection.insert_one(item_data).inserted_id

    # manufacturer = Manufacturer()
    # manufacturer.update(name, {"name": "Manufacturer Name", "description": "des 23"})
    def update(self, name, updates):
        collection = db["manufacturer"]
        update_data = {"$set": updates}
        result = collection.update_one({"name": name}, update_data)
        return result.modified_count

    # manufacturer = Manufacturer()
    # manufacturer.get(name)
    def get(self, name):
        collection = db["manufacturer"]
        manufacturer_data = collection.find_one({"name": name})
        return manufacturer_data

    # manufacturer = Manufacturer()
    # manufacturer.get_manufacturer()
    def get_manufacturers(self):
        collection = db["manufacturer"]
        items = collection.find()
        return [item for item in items]

    # manufacturer = Manufacturer()
    # manufacturer.delete(name)
    def delete(self, name):
        collection = db["manufacturer"]
        result = collection.delete_one({"name": name})
        return result.deleted_count


def register_manufacturer_model(db):
    collection_names = db.list_collection_names()
    if "manufacturer" not in collection_names:
        db.create_collection("manufacturer")
