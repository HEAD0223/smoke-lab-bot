from ..main import db


class Admin:
    # admin = Admin()
    # admin.create(user_id, username, email, language, created_at)
    def create(
        self,
        user_id,
        username,
        email,
        language=None,
        created_at=None,
    ):
        collection = db["admins"]
        admin_exists = collection.find_one({"user_id": user_id})
        if admin_exists:
            return None

        admin_data = {
            "user_id": user_id,
            "username": username,
            "email": email,
            "language": language,
            "created_at": created_at,
        }
        return collection.insert_one(admin_data).inserted_id

    # admin = Admin()
    # admin.update(user_id, {"language": "en", "phone": "123456789"})
    def update(self, user_id, updates):
        collection = db["admins"]
        update_data = {"$set": updates}
        result = collection.update_one({"user_id": int(user_id)}, update_data)
        return result.modified_count

    # admin = Admin()
    # admin.check(user_id, variable)
    def check(self, user_id, variable):
        collection = db["admins"]
        admin_data = collection.find_one({"user_id": user_id})
        if admin_data and variable in admin_data:
            return admin_data[variable]
        return None

    # admin = Admin()
    # admin.get(identifier)
    def get(self, identifier):
        collection = db["admins"]
        if identifier.isdigit():
            query = {"user_id": int(identifier)}
        else:
            query = {"username": identifier}
        admin_data = collection.find_one(query)
        return admin_data

    # admin = Admin()
    # admin.get_admins()
    def get_admins(self):
        collection = db["admins"]
        users = collection.find()
        return [user for user in users]

    # admin = Admin()
    # admin.get_lang(user_id)
    def get_lang(self, user_id):
        collection = db["admins"]
        admin_data = collection.find_one({"user_id": user_id})
        if admin_data and "language" in admin_data:
            return admin_data["language"]
        return None

    # admin = Admin()
    # admin.delete(user_id)
    def delete(self, user_id):
        collection = db["admins"]
        result = collection.delete_one({"user_id": user_id})
        return result.deleted_count


def register_admin_model(db):
    collection_names = db.list_collection_names()
    if "admins" not in collection_names:
        db.create_collection("admins")
