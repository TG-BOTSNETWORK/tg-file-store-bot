from pyrogram import Client, idle
from Config import config

tgbots = Client(
    ":memory:",  
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    bot_token=config.BOT_TOKEN,
    plugins=dict(root="plugins.modules"),
)

if __name__ == "__main__":
    print("Bot started!")
    tgbots.run()
