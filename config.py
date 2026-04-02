import os
from dotenv import load_dotenv

load_dotenv()

BERLIN_BOT_TOKEN  = os.getenv("BERLIN_BOT_TOKEN", "")
BERLIN_CHAT_ID    = os.getenv("BERLIN_CHAT_ID", "")

HAMBURG_BOT_TOKEN = os.getenv("HAMBURG_BOT_TOKEN", "")
HAMBURG_CHAT_ID   = os.getenv("HAMBURG_CHAT_ID", "")

REQUEST_TIMEOUT   = 15
SLEEP_BETWEEN     = 2
DB_PATH           = "seen.db"