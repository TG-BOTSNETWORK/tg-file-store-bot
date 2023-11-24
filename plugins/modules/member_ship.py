from pyrogram import Client, filters
from pyrogram.types import Message
from datetime import datetime, timedelta
from plugins.database.premium import add_premium_user, get_premium_users_count, delete_premium_user
from Config import config
from plugins import bot 

@bot.on_message(filters.command("addpremium") & filters.user(config.OWNER_ID))
async def addpremium(client: Client, message: Message):
    try:
        _, user_id, duration = message.text.split(" ", 2)
        user_id = int(user_id)
        duration = int(duration)
        expiration_date = datetime.utcnow() + timedelta(days=duration)
        add_premium_user(user_id)
        user_message = (
            f"Congratulations! You have been added as a premium user.\n\n"
            f"Enjoy your premium benefits until {expiration_date}.\n\n"
            "**Note:** If you engage in any scam or violate the rules, your premium status may be revoked at any time without notice. Be alert."
        )
        await client.send_message(user_id, user_message)

        await message.reply_text(f"User {user_id} added as premium until {expiration_date}.")
    except ValueError:
        await message.reply_text("Invalid command format. Use /addpremium user_id duration.")
    except Exception as e:
        print(e)
        await message.reply_text("Something went wrong.")

async def check_premium_expiration(client: Client, message: Message):
    expiration_date = datetime.utcnow() + timedelta(days=2)    
    premium_users = get_premium_users_count()    
    for user_id, expiration in premium_users.items():
        if expiration <= expiration_date:
            try:
                await client.send_message(user_id, "Your premium membership will expire in two days. renew fast")
            except Exception as e:
                print(e)

@bot.on_message(filters.command("getpremiumusers") & filters.user(config.OWNER_ID))
async def getpremiumusers(client: Client, message: Message):
    try:
        premium_users_count = get_premium_users_count()
        if premium_users_count == 0:
            await message.reply_text("No premium users found.")
        else:
            await message.reply_text(f"Total Premium Users: {premium_users_count}")
    except Exception as e:
        print(e)
        await message.reply_text("Something went wrong.")

@bot.on_message(filters.command("delpremiumuser") & filters.user(config.OWNER_ID))
async def delpremiumuser(client: Client, message: Message):
    try:
        _, user_id, reason = message.text.split(" ", 2)
        user_id = int(user_id)

        premium_users = get_premium_users_count()

        if not premium_users:
            await message.reply_text("No premium users found.")
            return

        if user_id not in premium_users:
            await message.reply_text(f"User {user_id} does not have premium membership.")
            return

        await client.send_message(user_id, f"Your premium membership has been revoked by bot owner.\n<b>Reason:</b> <code>{reason}</code>")
        delete_premium_user(user_id)
        await message.reply_text(f"User {user_id} deleted from premium users. Reason: {reason}")
    except ValueError:
        await message.reply_text("Invalid command format. Use /delpremiumuser user_id reason.")
    except Exception as e:
        print(e)
        await message.reply_text("Something went wrong.")
