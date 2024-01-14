from ..main import db


class Promo:
    # promo = Promo()
    # promo.create(user_id, promoName, usage, created_at)
    def create(
        self,
        user_id,
        promoName,
        usage,
        created_at,
    ):
        collection = db["promos"]

        promo_data = {
            "user_id": user_id,
            "promoName": promoName,
            "usage": usage,
            "created_at": created_at,
        }
        return collection.insert_one(promo_data).inserted_id

    # promo = Promo()
    # promo.update(promoName, {"usage": "100", "isAdmin": "false"})
    def update(self, promoName, updates):
        collection = db["promos"]
        update_data = {"$set": updates}
        result = collection.update_one({"promoName": promoName}, update_data)
        return result.modified_count

    # promo = Promo()
    # promo.check(promoName)
    def check(self, promoName):
        collection = db["promos"]
        promo_data = collection.find_one({"promoName": promoName})
        if promo_data:
            return True
        return False

    # promo = Promo()
    # promo.get(user_id)
    def get(self, user_id):
        collection = db["promos"]
        promo_data = collection.find({"user_id": int(user_id)})
        return list(promo_data)

    # promo = Promo()
    # promo.count(user_id)
    def count(self, user_id):
        collection = db["promos"]
        promo_count = collection.count_documents({"user_id": int(user_id)})
        return promo_count

    # promo = Promo()
    # promo.get_promos()
    def get_promos(self):
        collection = db["promos"]
        promos = collection.find()
        return [promo for promo in promos]

    # promo = Promo()
    # promo.delete(promoName)
    def delete(self, promoName):
        collection = db["promos"]
        result = collection.delete_one({"promoName": promoName})
        return result.deleted_count


def register_promo_model(db):
    collection_names = db.list_collection_names()
    if "promos" not in collection_names:
        db.create_collection("promos")
