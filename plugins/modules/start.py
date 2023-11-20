
from pyrogram import filters, Client 
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from plugins import corn 
from pyrogram.errors.exceptions import UserNotParticipant

force_channel = -1002119954783

start_keyboard = InlineKeyboardMarkup( [[
        InlineKeyboardButton("Help", callback_data="about"),
        InlineKeyboardButton("About", callback_data="about")
        ]]
        )
        
about_keyboard = InlineKeyboardMarkup( [[
       InlineKeyboardButton("⇦Back", callback_data="start")
       ]]
       )
              
@tgstore.on_message(filters.command("start") & filters.private)
async def start(corn, message: Message):
    if force_channel:
        try:
            user = await tgstore.get_chat_member(force_channel, message.from_user.id)
            if user.status == "kicked":
                await message.reply_text("You are banned.")
                return
        except UserNotParticipant:
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("Join Channel", url=f"https://t.me/TgBotsNetwork")]
            ])
            await message.reply_text("You are not joined in my channel. Please join the channel to use me.", reply_markup=keyboard)
            return

    await message.reply_text(f"Hello {message.from_user.mention}\n\nI am a private files save bot. I can save private files on certain channels, and other users can access them from a special link.", reply_markup=start_keyboard)

@tgstore.on_callback_query(filters.regex("about"))
async def about_callback(client, CallbackQuery):
    await CallbackQuery.edit_message_text(
        text="<b><u>About</u></b>\n\n<b>➺Bot Name:</b>[TG FILE STORING BOT](t.me/Tgfilestoringbot)\n<b>➺Language:</b>[python](https://python.org)\n<b>➺Library:</b>[pyrogram](https://pyrogram.org)\n<b>➺Devloped By:</b>[Nobitha](t.me/my_name_is_nobitha)", 
        disable_web_page_preview=True,    
        reply_markup=about_keyboard,
    )    

@tgstore.on_callback_query(filters.regex("start"))
async def start_callback(client, CallbackQuery):
    await CallbackQuery.edit_message_text(
        text=f"Hello {CallbackQuery.message.from_user.mention}\n\nI am a private files save bot. I can save private files on certain channels, and other users can access them from a special link.", 
        reply_markup=start_keyboard,
    )
