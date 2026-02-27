from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

import os

# Environment variables se credentials
api_id = int(os.environ.get("API_ID", "123456"))
api_hash = os.environ.get("API_HASH", "your_api_hash")
bot_token = os.environ.get("BOT_TOKEN", "your_bot_token")

# Bot client
app = Client("group_checker_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

# Minimum members required
REQUIRED_MEMBERS = 5

@app.on_message(filters.group & ~filters.service)
async def check_member_count(client, message):
    user = message.from_user
    chat = message.chat

    # Total members
    total_members = await client.get_chat_members_count(chat.id)

    if total_members - 1 < REQUIRED_MEMBERS:
        # Inline button to join group
        add_button = InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("Add Members ➕", url=f"https://t.me/{chat.username}")]
            ]
        )

        await message.reply_text(
            f"👤 {user.first_name}, pehle group me {REQUIRED_MEMBERS} member add karo, uske baad hi message kar paoge!",
            reply_markup=add_button
        )

app.run()
