from pyrogram import Client, filters, idle
from Config import config

with Client(
    ":tgstore:",
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    bot_token=config.BOT_TOKEN,
    plugins=dict(root="plugins.modules")
) as tgstore:
    print("Bot started!")
    tgstore.run()
