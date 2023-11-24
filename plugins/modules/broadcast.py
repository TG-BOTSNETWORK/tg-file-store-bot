from pyrogram import Client, filters
from pyrogram.types import Message
from plugins.database import get_users, get_chats
from plugins import bot as app
from Config import config

@app.on_message(filters.command("broadcast") & filters.user(config.OWNER_ID))
async def broadcast(client: Client, message: Message):
    try:
        text = message.text.split(" ", 1)[1]
        media = None
        if message.reply_to_message:
            media = message.reply_to_message.media
        users = get_users()
        chats = get_chats()
        for user_id in users:
            try:
                sent_message = await client.send_message(user_id, text, media=media)
                if "can_pin_messages" in sent_message.chat_permissions:
                    await client.pin_chat_message(user_id, sent_message.id)
                print(f"Broadcast sent to user: {user_id}")
            except Exception as e:
                print(f"Failed to send broadcast to user {user_id}: {e}")
        for chat_id in chats:
            try:
                sent_message = await client.send_message(chat_id, text, media=media)
                if "can_pin_messages" in sent_message.chat_permissions:
                    await client.pin_chat_message(chat_id, sent_message.id)
                print(f"Broadcast sent to chat: {chat_id}")
            except Exception as e:
                print(f"Failed to send broadcast to chat {chat_id}: {e}")

        await message.reply_text(f"Broadcast sent to {len(users)} users and {len(chats)} chats.")
    except IndexError:
        await message.reply_text("Invalid command format. Use /broadcast message.")
    except Exception as e:
        print(e)
        await message.reply_text("Something went wrong.")

if __name__ == "__main__":
    app.run()
