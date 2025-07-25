from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
import asyncio
from plugins import bot
from Config import config
import base64
from pyrogram.errors import FloodWait
from plugins.database.save_files_sql import add_total_files

DISABLE_CHANNEL_BUTTON = False

async def decode(base64_string):
    base64_string = base64_string.replace("Tgfilestore_", "")
    base64_bytes = base64_string.encode("ascii")
    string_bytes = base64.b64decode(base64_bytes)
    string = string_bytes.decode("utf-8")
    return string

async def encode(string):
    string_bytes = string.encode("ascii")
    base64_bytes = base64.b64encode(string_bytes)
    base64_string = base64_bytes.decode("ascii")
    return base64_string

@bot.on_message(filters.command('link') & filters.private)
async def link(client: Client, message: Message):
    if not message.reply_to_message or not message.reply_to_message.media:
        await message.reply_text("Please reply to a media message to generate a special link.")
        return
    
    reply_text = await message.reply_text("Please wait, your special link is generating...", quote=True)
    await reply_text.edit_text("Making a file id...")
    await asyncio.sleep(0.3)
    await reply_text.edit_text("Uploading your special link...")

    media_message = message.reply_to_message

    try:
        post_message = await media_message.copy(chat_id=client.db_channel.id, disable_notification=True)
    except FloodWait as e:
        await asyncio.sleep(e.x)
        post_message = await media_message.copy(chat_id=client.db_channel.id, disable_notification=True)
    except Exception as e:
        print(e)
        await reply_text.edit_text("Something went wrong while forwarding the media!")
        return

    converted_id = post_message.id * abs(client.db_channel.id)
    string = f"get-{converted_id}"

    base64_string = await encode(string)
    link = f"https://t.me/{client.username}?start={base64_string if 'Tgfilestore_' in base64_string else 'Tgfilestore_' + base64_string}"
    reply_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔁 Share URL", url=f'https://telegram.me/share/url?url={link}')]
    ])

    await reply_text.edit(
        f"<b>Here is your link</b>\n\n{link}",
        reply_markup=reply_markup,
        disable_web_page_preview=True
    )

    if not DISABLE_CHANNEL_BUTTON:
        user_id = message.from_user.id
        add_total_files(link, user_id)
        await post_message.edit_reply_markup(reply_markup)

@bot.on_message(filters.user(config.OWNER_ID) & filters.command("delfile") & filters.private)
async def delete_file(client: Client, message: Message):
    try:
        _, base64_string = message.text.split(" ", 1)
        base64_string = base64_string.replace("Tgfilestore_", "")
        string = await decode(base64_string)
        #add_deleted_files(string)    
        await message.reply_text(f"The file with special link '{string}' has been deleted.")
    except Exception as e:
        print(e)
        await message.reply_text("Something went wrong...!")
