from os import path, getenv
import os
from dotenv import load_dotenv

load_dotenv()



def is_enabled(value, default):
    if value.lower() in ["true", "yes", "1", "enable", "y"]:
        return True
    elif value.lower() in ["false", "no", "0", "disable", "n"]:
        return False
    else:
        return default



class config:

    API_ID = "8623612"
    API_HASH = "06ea2889c5517eb64017b032d667e29f"
    BOT_TOKEN = "6396685550:AAFhzt65XsaJYYUD0oG5ktgZVz4UHIQaOtg"
    SUDO_USERS = ["5857041668", "5810389985"]
    OWNER_ID = int(os.environ.get("OWNER_ID", "5857041668"))
    SUDO_USERS.append(OWNER_ID) if OWNER_ID not in SUDO_USERS else []
    CHANNELS = is_enabled((os.environ.get("CHANNELS", "True")), True)
    CHANNEL_ID = (
        [int(i.strip()) for i in os.environ.get("CHANNEL_ID", "-1002119954783").split(" ")]
        if os.environ.get("CHANNEL_ID")
        else []
    )
    DATABASE_URL = os.environ.get("DATABASE_URL", "postgres://askmadhi:OHHUSsmc7WUshSsgXGkjqPN5_0PGUX3-@berry.db.elephantsql.com/askmadhi")  
    BOT_USERNAME = os.environ.get("BOT_USERNAME", "TgfileStoringBot")
    DB_CHANNEL = int(os.environ.get("DB_CHANNEL", "-1002119954783"))
    LOG_CHANNEL = int(os.environ.get('LOG_CHANNEL', "-1002119954783"))
    FILE_STORE_CHANNEL = [int(ch) for ch in (os.environ.get('FILE_STORE_CHANNEL', '-1002119954783')).split()]
    PUBLIC_FILE_STORE = is_enabled(os.environ.get('PUBLIC_FILE_STORE', "True"), True)
    BOT_WORKERS = int(os.environ.get("BOT_WORKERS", "4"))
