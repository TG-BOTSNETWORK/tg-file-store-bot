from pyrogram import filters, Client
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from pyrogram.errors.exceptions import UserNotParticipant
from plugins import app 

force_channel_id = -1002119954783

start_keyboard = InlineKeyboardMarkup([[
    InlineKeyboardButton("Help", callback_data="help"),
    InlineKeyboardButton("About", callback_data="about")
]])

about_keyboard = InlineKeyboardMarkup([[
    InlineKeyboardButton("⇦Back", callback_data="start")
]])

help_keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("⇦Back", callback_data="start")]])

async def check_membership(user_id):
    try:
        member = await app.get_chat_member(force_channel_id, user_id)
        return member.status in ["member", "administrator", "creator"]
    except UserNotParticipant:
        return False

@app.on_message(filters.command(["start"]) & filters.private)
async def start(_, message: Message):
    if force_channel_id:
        if not await check_membership(message.from_user.id):
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("Join Channel", url=f"https://t.me/TgBotsNetwork")],
                [InlineKeyboardButton("Try Again", callback_data="again")]
            ])
            await message.reply_text(
                "You are not joined in my channel. Please join the channel to use me.",
                reply_markup=keyboard
            )
            return

    await message.reply_text(
        f"Hello {message.from_user.mention}\n\nI am a private files save bot. "
        "I can save private files on certain channels, and other users can access them from a special link.",
        reply_markup=start_keyboard
    )


@app.on_callback_query(filters.regex("about"))
async def about_callback(_, callback_query):
    await callback_query.edit_message_text(
        text="<b><u>About</u></b>\n\n<b>➺Bot Name:</b>[TG FILE STORING BOT](t.me/Tgfilestoringbot)\n"
             "<b>➺Language:</b>[python](https://python.org)\n<b>➺Library:</b>[pyrogram](https://pyrogram.org)\n"
             "<b>➺Developed By:</b>[Nobitha](t.me/my_name_is_nobitha)",
        disable_web_page_preview=True,
        reply_markup=about_keyboard,
    )

@app.on_callback_query(filters.regex("start"))
async def start_callback(_, callback_query):
    await callback_query.edit_message_text(
        text=f"Hello {callback_query.message.from_user.mention}\n\nI am a private files save bot. "
             "I can save private files on certain channels, and other users can access them from a special link.",
        reply_markup=start_keyboard,
    )

@app.on_callback_query(filters.regex("help"))
async def help_callback(_, callback_query):
    await callback_query.edit_message_text(
        text="Welcome to [TG FILE STORING BOT!](t.me/Tgfilestoringbot) Send any type of media, and I'll generate a special link for you.\n\n"
             "Commands:\n"
             "/start - Start using the bot\n"
             "/help - Display this help message\n"
             "<u>**Admin commands**</u>\n"
             "/broadcast - Broadcast a message to all users\n"
             "/stats - Display bot statistics\n"
             "/batch - Perform batch operations\n"
             "/genlink - Generate a special link for a file\n\n"
             "<u>**Note:**</u> if you want access admin commands by a premium membership",
        reply_markup=help_keyboard
    )

app.on_message(filters.command("help") & filters.private)
async def help(_, message: Message):
    await message.reply_text(
        "Welcome to [TG FILE STORING BOT!](t.me/Tgfilestoringbot) Send any type of media, and I'll generate a special link for you.\n\n"
        "Commands:\n"
        "/start - Start using the bot\n"
        "/help - Display this help message\n"
        "<u>**Admin commands**</u>\n"
        "/broadcast - Broadcast a message to all users\n"
        "/stats - Display bot statistics\n"
        "/batch - Perform batch operations\n"
        "/genlink - Generate a special link for a file\n\n"
        "<u>**Note:**</u> if you want access admin commands by a premium membership",
        reply_markup=help_keyboard
    )

@app.on_callback_query(filters.regex("again"))
async def again_callback(_, callback_query):
    if await check_membership(callback_query.from_user.id):
        await callback_query.edit_message_text(
            text=f"Hello {callback_query.from_user.mention}\n\nYou have successfully joined the channel! "
                 "Now you can use the bot to save private files on certain channels and access them from a special link.",
            reply_markup=start_keyboard
        )
    else:
        await callback_query.answer("Please join the channel to use the bot.")
