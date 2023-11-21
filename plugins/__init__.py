from pyrogram import Client
from Config import config

app = Client(
    ":storing:",  
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    bot_token=config.BOT_TOKEN,
    plugins=dict(root="plugins.modules"),
)

print("Bot started!")
app.start()
idle()
