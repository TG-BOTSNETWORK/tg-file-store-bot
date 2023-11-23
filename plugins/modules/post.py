from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
import asyncio
from plugins import bot
from Config import config
import base64
import re

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

@bot.on_message(filters.private & filters.user(config.OWNER_ID) & ~filters.command(['start', 'broadcast', 'batch', 'genlink', 'stats']))
async def channel_post(client: Client, message: Message):
    reply_text = await message.reply_text("Please wait, your special link is generating...", quote=True)
    await reply_text.edit_text("Making a file id...")
    await asyncio.sleep(0.3)
    await reply_text.edit_text("Uploading your special link...")
    
    try:
        post_message = await message.copy(chat_id=client.db_channel.id, disable_notification=True)
    except FloodWait as e:
        await asyncio.sleep(e.x)
        post_message = await message.copy(chat_id=client.db_channel.id, disable_notification=True)
    except Exception as e:
        print(e)
        await reply_text.edit_text("Something went wrong...!")
        return
    
    converted_id = post_message.id * abs(client.db_channel.id)
    string = f"get-{converted_id}"
    base64_string = await encode(string)
    link = f"https://t.me/{client.username}?start={base64_string if 'Tgfilestore_' in base64_string else 'Tgfilestore_' + base64_string}"

    user_details_message = f"<b>👤 User Details: 👤</b>\n\n" \
                           f"<b>👁 Uploaded By:</b> {user_details['uploaded_by']}\n" \
                           f"<b>🐧 User ID:</b> {user_details['user_id']}\n" \
                           f"<b>📂 Uploaded Files:</b> {', '.join(user_details['uploaded_files'])}\n" \
                           f"<b>💬 Channel Name:</b> {user_details['channel_name']}\n" \
                           f"<b>💽 Channel Username:</b> {user_details['channel_username']}\n" \
                           f"<b>📊 Channel ID:</b> {user_details['channel_id']}"

    await client.send_message(chat_id=CHANNEL_ID, text=user_details_message, disable_web_page_preview=True)

    callback_data = f"delete_link:{base64_string}" 
    reply_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔁 Share URL", url=f'https://telegram.me/share/url?url={link}')]
    ])

    await reply_text.edit(
        f"<b>Here is your link</b>\n\n{link}",
        reply_markup=reply_markup,
        disable_web_page_preview=True
    )

    if not DISABLE_CHANNEL_BUTTON:
        await post_message.edit_reply_markup(reply_markup)

@bot.on_message(filters.channel & filters.incoming & filters.chat(CHANNEL_ID))
async def new_post(client: Client, message: Message):
    if DISABLE_CHANNEL_BUTTON:
        return

    converted_id = message.id * abs(client.db_channel.id)
    string = f"get-{converted_id}"
    base64_string = await encode(string)
    link = f"https://t.me/{client.username}?start={base64_string if 'Tgfilestore_' in base64_string else 'Tgfilestore_' + base64_string}"
    
    reply_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔁 Share URL", url=f'https://telegram.me/share/url?url={link}')]
    ])
    
    try:
        await message.edit_reply_markup(reply_markup)
    except Exception as e:
        print(e)
        pass
