import os
import threading
from flask import Flask
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pymongo import MongoClient

# ================== CONFIG ==================

API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")
MONGO_URL = os.environ.get("MONGO_URL")

GROUP_ID = -1001551886347  # 👈 Apna group id yaha daalo
FORCE_LINK = "https://t.me/freindboss"  # 👈 Apna group link

# ============================================

# ================== FLASK WEB SERVER ==================

web_app = Flask(__name__)

@web_app.route("/")
def home():
    return "Bot & Website Running Successfully!"

def run_web():
    web_app.run(host="0.0.0.0", port=8000)

# ================== TELEGRAM BOT ==================

app = Client(
    "member-bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

mongo = MongoClient(MONGO_URL)
db = mongo["InviteBot"]
users = db["users"]

# ================== DATABASE FUNCTIONS ==================

async def get_invite_count(user_id):
    data = users.find_one({"user_id": user_id})
    if data:
        return data.get("invite", 0)
    return 0

async def add_invite(user_id):
    users.update_one(
        {"user_id": user_id},
        {"$inc": {"invite": 1}},
        upsert=True
    )

# ================== GROUP MESSAGE FILTER ==================

@app.on_message(filters.group & filters.text)
async def group_filter(client, message):

    if message.chat.id != GROUP_ID:
        return

    if not message.from_user:
        return

    user_id = message.from_user.id
    invite_count = await get_invite_count(user_id)

    if invite_count < 5:
        try:
            await message.delete()
        except:
            pass

        buttons = InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("📤 Share Link 1", url=FORCE_LINK)],
                [InlineKeyboardButton("📤 Share Link 2", url=FORCE_LINK)],
                [InlineKeyboardButton("📤 Share Link 3", url=FORCE_LINK)],
                [InlineKeyboardButton("📤 Share Link 4", url=FORCE_LINK)],
                [InlineKeyboardButton("📤 Share Link 5", url=FORCE_LINK)],
            ]
        )

        await message.reply_text(
            "❌ Is group pe aap SMS nahi kar sakte ho\n\n"
            "👉 Aapko pehle 5 member ko group ka link share karna hoga.",
            reply_markup=buttons
        )

# ================== START COMMAND ==================

@app.on_message(filters.private & filters.command("start"))
async def start_cmd(client, message):
    await message.reply_text(
        "👋 Welcome!\n\n"
        "Group me message bhejne ke liye 5 members invite karo."
    )

# ================== RUN BOTH ==================

def run_bot():
    app.run()

if __name__ == "__main__":
    t1 = threading.Thread(target=run_web)
    t1.start()
    run_bot()
