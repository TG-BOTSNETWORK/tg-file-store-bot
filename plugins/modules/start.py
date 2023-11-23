from pyrogram import filters, Client
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from pyrogram.errors.exceptions import UserNotParticipant
from plugins import bot
from plugins.database import add_user

start_keyboard = InlineKeyboardMarkup([[
    InlineKeyboardButton("Help", callback_data="help"),
    InlineKeyboardButton("About", callback_data="about")
]])

about_keyboard = InlineKeyboardMarkup([[
    InlineKeyboardButton("⇦Back", callback_data="start")
]])

help_keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("⇦Back", callback_data="start")]])

@bot.on_message(filters.command("start") & filters.private)
async def start(_, message: Message):
    add_user(message.from_user.id)
    text = message.text
    if len(text) > 7:
        try:
            base64_string = text.split(" ", 1)[1]
        except:
            return
        string = await decode(base64_string)
        argument = string.split("-")
        if len(argument) == 3:
            try:
                start = int(int(argument[1]) / abs(client.db_channel.id))
                end = int(int(argument[2]) / abs(client.db_channel.id))
            except:
                return
            if start <= end:
                ids = range(start, end + 1)
            else:
                ids = []
                i = start
                while True:
                    ids.append(i)
                    i -= 1
                    if i < end:
                        break
        elif len(argument) == 2:
            try:
                ids = [int(int(argument[1]) / abs(client.db_channel.id))]
            except:
                return
        temp_msg = await message.reply("Please wait...")
        try:
            messages = await get_messages(client, ids)
        except:
            await message.reply_text("Something went wrong..!")
            return
        await temp_msg.delete()
        await message.reply_text(
            f"Hello {message.from_user.mention}\n\nI am a private files save bot. "
            "I can save private files on certain channels, and other users can access them from a special link.",
            reply_markup=start_keyboard
        )

@bot.on_callback_query(filters.regex("about"))
async def about_callback(_, callback_query):
    await callback_query.edit_message_text(
        text="<b><u>About</u></b>\n\n<b>➺Bot Name:</b>[TG FILE STORING BOT](t.me/Tgfilestoringbot)\n"
             "<b>➺Language:</b>[python](https://python.org)\n<b>➺Library:</b>[pyrogram](https://pyrogram.org)\n"
             "<b>➺Developed By:</b>[Nobitha](t.me/my_name_is_nobitha)",
        disable_web_page_preview=True,
        reply_markup=about_keyboard,
    )

@bot.on_callback_query(filters.regex("start"))
async def start_callback(_, callback_query):
    await callback_query.edit_message_text(
        text=f"Hello {callback_query.message.from_user.mention}\n\nI am a private files save bot. "
             "I can save private files on certain channels, and other users can access them from a special link.",
        reply_markup=start_keyboard,
    )

@bot.on_callback_query(filters.regex("help"))
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

@bot.on_message(filters.command("help") & filters.private)
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
