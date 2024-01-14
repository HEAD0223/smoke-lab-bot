from bot.misc import TgKeys
from pymongo import MongoClient

url = (
    "mongodb+srv://"
    + TgKeys.HOST_DB
    + ":"
    + TgKeys.PASSWORD_DB
    + "@cluster0.56elheg.mongodb.net/?retryWrites=true&w=majority"
)


# Establish a connection to MongoDB
client = MongoClient(url)
db = client["smoke-lab"]


admin_list = [382586338]
