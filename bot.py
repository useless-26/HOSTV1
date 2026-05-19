import os
import logging
from pyrogram import Client
from aiohttp import web
import asyncio

# Environment variables
API_ID = int(os.environ.get("API_ID", 0))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")

# Logging
logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)

# Create bot
bot = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@bot.on_message()
async def handle_message(client, message):
    await message.reply("✅ Bot is alive on Render!")

async def main():
    # Start web server for health checks (Required for Render)
    web_app = web.Application()
    
    async def health_check(request):
        return web.Response(text="Bot is running")
    
    web_app.router.add_get("/", health_check)
    
    # Bind to PORT environment variable
    port = int(os.environ.get("PORT", 10000))
    runner = web.AppRunner(web_app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()
    
    LOGGER.info(f"✅ Web server started on port {port}")
    LOGGER.info("✅ Bot is starting...")
    
    # Start bot
    await bot.start()
    LOGGER.info("✅ Bot started successfully!")
    
    # Keep everything running
    await asyncio.Future()  # Run forever

if __name__ == "__main__":
    if not all([API_ID, API_HASH, BOT_TOKEN]):
        LOGGER.error("❌ Missing environment variables!")
        LOGGER.info("Set API_ID, API_HASH, BOT_TOKEN in Render Dashboard")
        exit(1)
    
    asyncio.run(main())
