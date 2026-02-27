@app.on_message(filters.group & filters.text)
async def check_access(client, message):
    user_id = message.from_user.id
    first_name = message.from_user.first_name

    # Correct: await inside async function
    bot_info = await client.get_me()
    referral_link = f"https://t.me/{bot_info.username}?start={user_id}"

    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "📤 Share 5 Members",
                    url=f"https://t.me/share/url?url={referral_link}&text=Is group me join karein aur maza lein 🔥"
                )
            ],
            [
                InlineKeyboardButton(
                    "🔗 Group Join Karein",
                    url=GROUP_LINK
                )
            ]
        ]
    )

    await message.reply_text(
        f"Namaste [{first_name}](tg://user?id={user_id}) 👋\n\n"
        f"Group me message karne ke liye aapko 5 members invite karne honge.\n\n"
        f"Apna invite link share karein aur referral se 5 log join karne ke baad hi aap chat kar paayenge:\n{referral_link}",
        reply_markup=keyboard,
        disable_web_page_preview=True
    )
