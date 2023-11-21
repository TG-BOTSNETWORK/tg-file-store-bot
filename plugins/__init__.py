from pyrogram import Client, idle
from Config import config

bot = Client(
    ":santhu:",  
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    bot_token=config.BOT_TOKEN,
    plugins=dict(root="plugins.modules"),
)

