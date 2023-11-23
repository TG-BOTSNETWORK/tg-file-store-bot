from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from plugins import bot 
from plugins.database import add_user, add_chat, get_users, get_chats
from plugins.database.premium import add_premium_user, get_premium_users, delete_premium_user


@bot.on_command("stats", filters.private)
def stats_command(client, message):
    if message.from_user.id == config.OWNER_ID:  
        total_users = get_users()
        total_chats = get_chats()
        total_premium_users = get_premium_users()

        message.reply_text(
            f"Total Users: {total_users}\nTotal Chats: {total_chats}\nTotal Premium Users: {total_premium_users}"
        )
    else:
        message.reply_text("You are not authorized to use this command.")
