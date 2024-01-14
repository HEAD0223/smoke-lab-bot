from ..main import db


class User:
    # user = User()
    # user.create(user_id, username, language, created_at, points, purchase_amount)
    def create(
        self,
        user_id,
        username,
        language=None,
        created_at=None,
        points=0,
        purchase_amount=0,
    ):
        collection = db["users"]
        user_exists = collection.find_one({"user_id": user_id})
        if user_exists:
            return None

        user_data = {
            "user_id": user_id,
            "username": username,
            "language": language,
            "created_at": created_at,
            "points": points,
            "purchase_amount": purchase_amount,
        }
        return collection.insert_one(user_data).inserted_id

    # user = User()
    # user.update(user_id, {"language": "en", "phone": "123456789"})
    def update(self, user_id, updates):
        collection = db["users"]
        update_data = {"$set": updates}
        result = collection.update_one({"user_id": int(user_id)}, update_data)
        return result.modified_count

    # user = User()
    # user.check(user_id, variable)
    def check(self, user_id, variable):
        collection = db["users"]
        user_data = collection.find_one({"user_id": user_id})
        if user_data and variable in user_data:
            return user_data[variable]
        return None

    # user = User()
    # user.get(identifier)
    def get(self, identifier):
        collection = db["users"]
        if identifier.isdigit():
            query = {"user_id": int(identifier)}
        else:
            query = {"username": identifier}
        user_data = collection.find_one(query)
        return user_data

    # user = User()
    # user.get_users()
    def get_users(self):
        collection = db["users"]
        users = collection.find()
        return [user for user in users]

    # user = User()
    # user.get_lang(user_id)
    def get_lang(self, user_id):
        collection = db["users"]
        admin_data = collection.find_one({"user_id": user_id})
        if admin_data and "language" in admin_data:
            return admin_data["language"]
        return None

    # user = User()
    # user.get_users_count()
    def get_users_count(self):
        collection = db["users"]
        count = collection.count_documents({})
        return count


def register_user_model(db):
    collection_names = db.list_collection_names()
    if "users" not in collection_names:
        db.create_collection("users")
