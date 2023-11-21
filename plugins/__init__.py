from pyrogram import Client, idle
from Config import config

tgbots = Client(
    ":tgbots:",  
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    bot_token=config.BOT_TOKEN,
    plugins=dict(root="plugins.modules"),
)

print("Bot started!")
tgbots.start()
idle()
