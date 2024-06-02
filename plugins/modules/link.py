import asyncio
import re
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from plugins import bot
from Config import config
from plugins.modules.post import encode
from pyrogram.errors import FloodWait

async def get_messages(client, message_ids):
    messages = []
    total_messages = 0
    while total_messages != len(message_ids):
        temp_ids = message_ids[total_messages:total_messages+200]
        try:
            msgs = await client.get_messages(
                chat_id=client.db_channel.id,
                message_ids=temp_ids
            )
        except FloodWait as e:
            await asyncio.sleep(e.x)
            msgs = await client.get_messages(
                chat_id=client.db_channel.id,
                message_ids=temp_ids
            )
        except:
            pass
        total_messages += len(temp_ids)
        messages.extend(msgs)
    return messages

async def get_message_id(client, message):
    if message.text:
        pattern = r"https://t.me/(?:c/)?(.*)/(\d+)"
        matches = re.match(pattern, message.text)
        if not matches:
            return 0
        channel_id = matches.group(1)
        msg_id = int(matches.group(2))
        if channel_id.isdigit():
            if f"-100{channel_id}" == str(client.db_channel.id):
                return msg_id
        else:
            if channel_id == client.db_channel.username:
                return msg_id
    elif message.reply_to_message:
        if message.reply_to_message.forward_from_chat:
            if message.reply_to_message.forward_from_chat.id == client.db_channel.id:
                return message.reply_to_message.forward_from_message_id
        elif message.reply_to_message.text:
            pattern = r"https://t.me/(?:c/)?(.*)/(\d+)"
            matches = re.match(pattern, message.reply_to_message.text)
            if not matches:
                return 0
            channel_id = matches.group(1)
            msg_id = int(matches.group(2))
            if channel_id.isdigit():
                if f"-100{channel_id}" == str(client.db_channel.id):
                    return msg_id
            else:
                if channel_id == client.db_channel.username:
                    return msg_id
    return 0

def get_readable_time(seconds: int) -> str:
    count = 0
    up_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "h", "days"]
    while count < 4:
        count += 1
        remainder, result = divmod(seconds, 60) if count < 3 else divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)
    time_list.reverse()
    for i, time_val in enumerate(time_list):
        up_time += f"{time_val}{time_suffix_list[i]}"
        if i < len(time_list) - 1:
            up_time += ":"
    return up_time

@bot.on_message(filters.private & filters.user(config.OWNER_ID) & filters.command('batch'))
async def batch(bot, message: Message):
    while True:
        try:
            first_message = await bot.ask(
                text="Reply to the first message of the album or multiple files in DB Channel..",
                chat_id=message.from_user.id,
                filters=(filters.reply & ~filters.forwarded),
                timeout=60
            )
        except:
            return

        f_msg_id = await get_message_id(bot, first_message)
        if f_msg_id:
            break
        else:
            await first_message.reply("❌ Error\n\nThis message is not from my DB Channel or this link is invalid.", quote=True)
            continue

    while True:
        try:
            second_message = await bot.ask(
                text="Reply to the last message of the album or multiple files in DB Channel..",
                chat_id=message.from_user.id,
                filters=(filters.reply & ~filters.forwarded),
                timeout=60
            )
        except:
            return

        s_msg_id = await get_message_id(bot, second_message)
        if s_msg_id:
            break
        else:
            await second_message.reply("❌ Error\n\nThis message is not from my DB Channel or this link is invalid.", quote=True)
            continue

    string = f"get-{f_msg_id * abs(bot.db_channel.id)}-{s_msg_id * abs(bot.db_channel.id)}"
    base64_string = await encode(string)
    link = f"https://t.me/{bot.username}?start={base64_string if 'littlehimeko_' in base64_string else 'littlehimeko_' + base64_string}"
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("🔁 Share URL", url=f'https://telegram.me/share/url?url={link}')]])
    await second_message.reply_text(f"<b>Here is your link</b>\n\n{link}", quote=True, reply_markup=reply_markup)

@bot.on_message(filters.private & filters.user(config.OWNER_ID) & filters.command('genlink'))
async def link_generator(bot, message: Message):
    while True:
        try:
            channel_message = await bot.ask(
                text="Reply to the message of the album or multiple files in DB Channel..",
                chat_id=message.from_user.id,
                filters=(filters.reply & ~filters.forwarded),
                timeout=60
            )
        except:
            return

        msg_id = await get_message_id(bot, channel_message)
        if msg_id:
            break
        else:
            await channel_message.reply("❌ Error\n\nThis message is not from my DB Channel or this link is invalid.", quote=True)
            continue

    base64_string = await encode(f"get-{msg_id * abs(bot.db_channel.id)}")
    link = f"https://t.me/{bot.username}?start={base64_string if 'littlehimeko_' in base64_string else 'littlehimeko_' + base64_string}"
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("🔁 Share URL", url=f'https://telegram.me/share/url?url={link}')]])
    await channel_message.reply_text(f"<b>Here is your link</b>\n\n{link}", quote=True, reply_markup=reply_markup)
