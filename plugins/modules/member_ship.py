#TgBotsNetwork

from pyrogram import Client, filters
from pyrogram.types import Message
from datetime import datetime, timedelta
from plugins.database.premium import add_premium_user, get_premium_users_count, delete_premium_user
from Config import config
from plugins import bot 
import random 
import string

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
        premium_users_count = get_premium_users_count()
        if premium_users_count == 0:
            await message.reply_text("No premium users found.")
            return
        delete_premium_user(user_id)
        await client.send_message(user_id, f"Your premium membership has been revoked by bot owner.\n<b>Reason:</b> <code>{reason}</code>")
        await message.reply_text(f"User {user_id} deleted from premium users.\n<b>Reason:</b> <code>{reason}</code>")
    except ValueError:
        await message.reply_text("Invalid command format. Use /delpremiumuser user_id reason.")
    except Exception as e:
        print(e)
        await message.reply_text("Something went wrong.")
        
##############################################  Soon ###################################################################
@bot.on_message(filters.command("redeemcode") & filters.user(config.OWNER_ID))
async def redeemcode(client: Client, message: Message):
    try:
        _, duration, limit = message.text.split(" ", 2)
        limit = int(limit)
        code_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        expiration_date = datetime.utcnow() + timedelta(days=int(duration))
        # Save the redeem code and limit in your database
        #save_redeem_code(f"TG_FILE_STORE_{code_id}", expiration_date, limit)
        await message.reply_text(f"Redeem code generated: <code>TG_FILE_STORE_{code_id}</code>\n"
                                  f"Expires: {expiration_date}\n"
                                  f"Limit: {limit}")
    except ValueError:
        await message.reply_text("Invalid command format. Use /redeemcode duration limit.")
    except Exception as e:
        print(e)
        await message.reply_text("Something went wrong.")

#@bot.on_message(filters.command("redeem") & filters.private)
#async def redeem(client: Client, message: Message):
#    try:
#        _, code = message.text.split(" ", 1)
#        user_id = message.from_user.id
#        if is_valid_redeem_code(code) and not has_exceeded_limit(code):
#            add_premium_user(user_id, get_redeem_code_expiration(code))
#            increment_redeem_code_usage(code)
#            await message.reply_text("Congratulations! You have redeemed a premium code to access premium contact @my_names_is_nobitha with redemed screen shot.")
#        else:
#            await message.reply_text("Invalid or expired redeem code.")
#    except ValueError:
#        await message.reply_text("Invalid command format. Use /redeem code.")
#    except Exception as e:
#        print(e)
#        await message.reply_text("Something went wrong.")
