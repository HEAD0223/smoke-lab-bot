from os import environ

# # DEV
# from dotenv import load_dotenv

# load_dotenv()
# # DEV


class TgKeys:
    TOKEN = environ.get("TOKEN", "define me!")
    HOST_DB = environ.get("HOST_DB", "define me!")
    PASSWORD_DB = environ.get("PASSWORD_DB", "define me!")
