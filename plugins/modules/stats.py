from pyrogram import Client, filters, __version__
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from plugins import bot 
from plugins.database import add_user, add_chat, get_users, get_chats
from plugins.database.save_files_sql import add_total_files, add_saved_files, add_deleted_files
from plugins.database.premium import add_premium_user, get_premium_users, delete_premium_user
from Config import config

cls_keyboard = InlineKeyboardMarkup(
    [[InlineKeyboardButton("Close", callback_data="close")]]
)

@bot.on_message(filters.command("stats"))
def stats(bot, message):
    if message.from_user.id == config.SUDO_USERS:
        keyboard = InlineKeyboardMarkup(
            [[InlineKeyboardButton("See Full Stats", callback_data="see_full_stats")]]
        )
        message.reply_text(
            "Click the button below to see full stats.",
            reply_markup=keyboard
        )
    else:
        message.reply_text("You are not authorized to use this command.")

@bot.on_callback_query(filters.regex("see_full_stats"))
def see_full_stats(bot, callback_query):
    if callback_query.from_user.id == config.OWNER_ID:
        total_users = get_users()
        total_chats = get_chats()
        total_premium_users = get_premium_users()

        stats_text = (
            f"**Total Users:** `{total_users}`\n"
            f"**Total Chats:** `{total_chats}`\n"
            f"**Total Premium Users:** `{total_premium_users}`\n"
            f"**Uploaded Files:** `{add_total_files()}`\n"
            f"**Saved Files:** `{add_saved_files()}`\n"
            f"**Deleted Files:** `{add_deleted_files()}`\n"
            f"**Pyrogram Version:** `{__version__}`"
        )

        callback_query.edit_message_text(stats_text, reply_markup=cls_keyboard)
    else:
        callback_query.answer("You are not authorized to use this button.", show_alert=True)
