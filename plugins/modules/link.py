from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto, InputMediaVideo
from Config import config
from plugins.modules.post import encode
from pyrogram.errors import FloodWait
import asyncio
import re

@Client.on_message(filters.user(config.OWNER_ID) & filters.command("batch") & filters.reply)
async def batch(bot: Client, message: Message):
    if not message.reply_to_message or not message.reply_to_message.media_group_id:
        await message.reply("Please reply to a media album.")
        return
    media_group_id = message.reply_to_message.media_group_id
    media_album = await bot.get_media_group(
        chat_id=message.chat.id, 
        message_id=message.reply_to_message.id
    )  
    editable = await message.reply("Processing your request...")

    try:
        sent_album = await forward_media_group(bot, media_album, editable)
    except Exception as e:
        await editable.edit(f"Failed to forward media album: {e}")
        return

    if not sent_album:
        await editable.edit("Failed to forward the media album.")
        return
    post_message = sent_album[0]
    media_ids = [msg.id for msg in sent_album]
    media_ids_str = "-".join(map(str, media_ids))
    converted_id = post_message.id * abs(bot.db_channel.id)
    string = f"get-{converted_id}-{media_ids_str}"
    base64_string = await encode(string)
    link = f"https://t.me/{bot.username}?start={base64_string if 'Tgfilestore_' in base64_string else 'Tgfilestore_' + base64_string}"
    await editable.edit(
        f"Here is your album link: {link}",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("Open Album", url=link)]]
        ),
        disable_web_page_preview=True
    )

async def forward_media_group(bot: Client, media_album, editable: Message):
    try:
        if all(media.photo for media in media_album):
            media_inputs = [InputMediaPhoto(media.photo.file_id, caption=(media.caption if media == media_album[0] else "")) for media in media_album]
        elif all(media.video for media in media_album):
            media_inputs = [InputMediaVideo(media.video.file_id, caption=(media.caption if media == media_album[0] else "")) for media in media_album]
        else:
            raise ValueError("Mixed media types in the album are not supported")

        sent_album = await bot.send_media_group(chat_id=config.DB_CHANNEL, media=media_inputs)
        return sent_album
    except Exception as e:
        await editable.edit(f"Failed to forward media group: {e}")
        return None

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
        except Exception as e:
            print(f"Error while fetching messages: {e}")
            break
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
