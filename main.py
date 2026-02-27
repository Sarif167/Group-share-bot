referral_link = f"https://t.me/{(await client.get_me()).username}?start={user_id}"

keyboard = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(
                "📤 Share 5 Member",
                url=f"https://t.me/share/url?url={referral_link}&text=Is group ko join karein aur maza lein 🔥"
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
    f"Apna invite link share karein:\n{referral_link}\n\n"
    f"Jab 5 log join kar lenge tab aap message kar paayenge.",
    reply_markup=keyboard,
    disable_web_page_preview=True
)
