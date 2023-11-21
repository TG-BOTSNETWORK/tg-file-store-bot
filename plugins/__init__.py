from pyrogram import Client
from Config import config

tgstore = Client(
    session_name=":storing:",  # Set a unique session name
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    bot_token=config.BOT_TOKEN,
    plugins=dict(root="plugins.modules"),
    storage=dict(is_memory=True)  
)

print("Bot started!")
tgstore.start()
idle()
