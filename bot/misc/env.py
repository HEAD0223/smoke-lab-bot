from os import environ
from typing import Final

# DEV
from dotenv import load_dotenv

load_dotenv()
# DEV


class TgKeys:
    TOKEN: Final = environ.get("TOKEN", "define me!")
    HOST_DB: Final = environ.get("HOST_DB", "define me!")
    PASSWORD_DB: Final = environ.get("PASSWORD_DB", "define me!")
