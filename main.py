import os
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from motor.motor_asyncio import AsyncIOMotorClient
from flask import Flask
from threading import Thread
from config import *

app = Client("referral_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

mongo = AsyncIOMotorClient(MONGO_URI)
db = mongo["referral_bot"]
users = db.users

# Flask for Koyeb health check
flask_app = Flask(__name__)

@flask_app.route("/")
def home():
    return "Bot Running"

def run():
    flask_app.run(host="0.0.0.0", port=8000)

# Start command with referral
@app.on_message(filters.private & filters.command("start"))
async def start(client, message):
    user_id = message.from_user.id
    first_name = message.from_user.first_name

    referrer = None
    if len(message.command) > 1:
        referrer = int(message.command[1])

    user_data = await users.find_one({"user_id": user_id})

    if not user_data:
        await users.insert_one({
            "user_id": user_id,
            "referrals": 0,
            "referred_by": referrer,
            "verified": False
        })

        if referrer and referrer != user_id:
            await users.update_one(
                {"user_id": referrer},
                {"$inc": {"referrals": 1}}
            )

    referral_link = f"https://t.me/{(await client.get_me()).username}?start={user_id}"

    await message.reply_text(
        f"Hello {first_name} 👋\n\n"
        f"Invite {REQUIRED_REFERRALS} friends using your link to unlock group chat.\n\n"
        f"Your Link:\n{referral_link}",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("🔗 Join Group", url=GROUP_LINK)]]
        )
    )

# Check group messages
@app.on_message(filters.group & filters.text)
async def check_access(client, message):
    user_id = message.from_user.id
    first_name = message.from_user.first_name

    user_data = await users.find_one({"user_id": user_id})

    if not user_data or user_data["referrals"] < REQUIRED_REFERRALS:
        await message.delete()

        referral_link = f"https://t.me/{(await client.get_me()).username}?start={user_id}"

        await message.reply_text(
            f"Hello [{first_name}](tg://user?id={user_id}) 👋\n\n"
            f"You need {REQUIRED_REFERRALS} referrals to chat.\n"
            f"Share your link with real members:\n{referral_link}",
            disable_web_page_preview=True
        )
    else:
        await client.restrict_chat_member(
            GROUP_ID,
            user_id,
            permissions=None
        )

if __name__ == "__main__":
    Thread(target=run).start()
    app.run()
