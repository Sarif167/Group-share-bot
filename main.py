import os
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from motor.motor_asyncio import AsyncIOMotorClient
from flask import Flask
from threading import Thread
from config import *

# Bot and DB setup
app = Client("referral_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
mongo = AsyncIOMotorClient(MONGO_URI)
db = mongo["referral_bot"]
users = db.users

# Flask for Koyeb health check
flask_app = Flask(__name__)

@flask_app.route("/")
def home():
    return "Bot Running!"

def run_flask():
    flask_app.run(host="0.0.0.0", port=8000)

# Helper: Create referral link
async def get_referral_link(client, user_id):
    bot_info = await client.get_me()
    return f"https://t.me/{bot_info.username}?start={user_id}"

# Group message handler
@app.on_message(filters.group & filters.text)
async def check_access(client, message):
    user_id = message.from_user.id
    first_name = message.from_user.first_name

    # Check DB for referrals
    user_data = await users.find_one({"user_id": user_id})
    if not user_data or user_data.get("referrals", 0) < REQUIRED_REFERRALS:
        # Auto delete member message
        await message.delete()

        # Generate referral link
        referral_link = await get_referral_link(client, user_id)

        # Reply with profile name + buttons
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "📤 Share 5 Members",
                        url=f"https://t.me/share/url?url={referral_link}&text=Join this group using my referral link!"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "🔗 Join Group",
                        url=GROUP_LINK
                    )
                ]
            ]
        )

        await message.reply_text(
            f"Namaste [{first_name}](tg://user?id={user_id}) 👋\n\n"
            f"Group me message karne ke liye aapko 5 members invite karne honge.\n\n"
            f"Apna invite link share karein aur jab 5 log join ho jayenge tab aap message kar paayenge:\n{referral_link}",
            reply_markup=keyboard,
            disable_web_page_preview=True
        )

# Start Flask + Bot
if __name__ == "__main__":
    Thread(target=run_flask).start()
    app.run()
