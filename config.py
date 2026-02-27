import os

API_ID = int(os.environ.get("API_ID", 0))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")
MONGO_URI = os.environ.get("MONGO_URI")
GROUP_ID = int(os.environ.get("GROUP_ID", 0))
GROUP_LINK = os.environ.get("GROUP_LINK")

REQUIRED_REFERRALS = 5
