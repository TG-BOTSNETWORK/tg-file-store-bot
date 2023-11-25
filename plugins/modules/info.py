from pyrogram import Client, filters
from pyrogram.types import Message, User
from datetime import datetime
import os
from plugins import bot as app
from pyrogram.enums import ParseMode

def get_user_info(user: User):
    user_info = (
        f"<b>Mention:</b> {user.mention}\n"
        f"<b>Username:</b> @{user.username}\n"
        f"<b>ID:</b> <code>{user.id}</code>\n"
        f"<b>Profile Link:</b> <a href='tg://user?id={user.id}'><b>Click Here</b></a>\n"
        f"<b>Is Scam:</b> {'Yes' if user.is_scam else 'No'}\n"
        f"<b>Is Premium:</b> {'Yes' if user.is_premium else 'No'}\n"
        f"<b>Last Seen:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    )
    return user_info

@app.on_message(filters.command("info"))
async def info_command(client: Client, message: Message):
    try:
        msg = await message.edit_text("Searching user ID...")
        user_id = int(message.text.split(" ", 1)[1]) if len(message.text.split(" ", 1)) > 1 else None
        if user_id:
            await msg.edit_text("Getting user info...")
            user = await client.get_users(user_id)
            user_info = get_user_info(user)
            profile_pic = await client.download_media(user.photo.big_file_id) if user.photo else None
            await msg.edit_text("Uploading user info...")
            await message.reply_photo(photo=profile_pic, caption=user_info, parse_mode=ParseMode.HTML)
            if profile_pic:
                os.remove(profile_pic)
        else:
            await msg.edit_text("Getting user info...")
            user_info = get_user_info(message.from_user)
            profile_pic = await client.download_media(message.from_user.photo.big_file_id) if message.from_user.photo else None
            await msg.edit_text("Uploading user info...")
            await message.reply_photo(photo=profile_pic, caption=user_info, parse_mode=ParseMode.HTML)
            if profile_pic:
                os.remove(profile_pic)
    except ValueError:
        await message.reply_text("Invalid user ID. Please provide a valid numerical user ID.")
    except Exception as e:
        print(e)
        await message.reply_text(f"Something went wrong: {e}")
