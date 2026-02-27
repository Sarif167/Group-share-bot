import os

API_ID = int(os.getenv("API_ID", 0))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
MONGO_URI = os.getenv("MONGO_URI")
GROUP_ID = int(os.getenv("GROUP_ID", 0))
GROUP_LINK = os.getenv("GROUP_LINK")

REQUIRED_REFERRALS = 5
