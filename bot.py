import os
from pyrogram import Client

# Read environment variables
API_ID = int(os.environ.get("API_ID", 0))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")

# Simple bot
app = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message()
async def reply(client, message):
    await message.reply("✅ Bot is working!")

print("Bot starting...")
app.run()
