from pyrogram import filters, Client
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from pyrogram.errors.exceptions import UserNotParticipant
from plugins import bot
from plugins.database import add_user
from plugins.modules.post import decode, DISABLE_CHANNEL_BUTTON
from plugins.modules.link import get_messages
import os
from pyrogram.errors import FloodWait

start_keyboard = InlineKeyboardMarkup([[
    InlineKeyboardButton("Help", callback_data="help"),
    InlineKeyboardButton("About", callback_data="about")
]])

about_keyboard = InlineKeyboardMarkup([[
    InlineKeyboardButton("⇦Back", callback_data="start")
]])

help_keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("⇦Back", callback_data="start")]])

PROTECT_CONTENT = True if os.environ.get('PROTECT_CONTENT', "False") == "True" else False
CUSTOM_CAPTION = os.environ.get("CUSTOM_CAPTION", None)

@bot.on_message(filters.command("start") & filters.private)
async def start_command(client, message: Message):
    add_user(message.from_user.id)
    text = message.text

    if len(text) > 7:
        try:
            base64_string = text.split(" ", 1)[1]
        except IndexError:
            return

        string = await decode(base64_string)
        argument = string.split("-")

        if len(argument) == 3:
            try:
                start = int(int(argument[1]) / abs(client.db_channel.id))
                end = int(int(argument[2]) / abs(client.db_channel.id))
            except ValueError:
                return

            ids = list(range(start, end + 1))

        elif len(argument) == 2:
            try:
                ids = [int(int(argument[1]) / abs(client.db_channel.id))]
            except ValueError:
                return

        temp_msg = await message.reply("Please wait...")

        try:
            messages = await get_messages(client, ids)
        except Exception:
            await message.reply_text("Something went wrong..!")
            return

        await temp_msg.delete()

        for msg in messages:
            if bool(CUSTOM_CAPTION) and bool(msg.document):
                caption = CUSTOM_CAPTION.format(
                    previouscaption="" if not msg.caption else msg.caption.html,
                    filename=msg.document.file_name
                )
            else:
                caption = "" if not msg.caption else msg.caption.html

            if DISABLE_CHANNEL_BUTTON:
                reply_markup = msg.reply_markup
            else:
                reply_markup = None

            try:
                await msg.copy(
                    chat_id=message.from_user.id,
                    caption=caption,
                    parse_mode=ParseMode.HTML,
                    reply_markup=start_keyboard,
                    protect_content=PROTECT_CONTENT
                )
                await asyncio.sleep(0.5)
            except FloodWait as e:
                await asyncio.sleep(e.x)
                await msg.copy(
                    chat_id=message.from_user.id,
                    caption=caption,
                    parse_mode=ParseMode.HTML,
                    reply_markup=start_keyboard,
                    protect_content=PROTECT_CONTENT
                )
            except Exception:
                pass
        return

    else:
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
