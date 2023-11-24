from pyrogram import Client, filters
from pyrogram.types import Chat, Message
from plugins.database import add_chat
from plugins import bot

@bot.on_chat_member()
async def on_chat_member_added(client: Client, message: Message):
    if message.new_chat_members:
        for member in message.new_chat_members:
            if member.id == client.get_me().id:
                chat_id = message.chat.id
                add_chat(chat_id)
                await message.reply_text(f"Thanks for adding me to this chat! but iam work for my owner only")
